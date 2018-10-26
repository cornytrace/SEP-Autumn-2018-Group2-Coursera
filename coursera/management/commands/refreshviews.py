from time import time

from django.core.management.base import BaseCommand
from django.db import connection, transaction
from psycopg2 import sql
from psycopg2.extensions import quote_ident

RECURSIVE_VIEWS_QUERY = """
WITH RECURSIVE matview_dependencies AS (
    SELECT
        matviewname,
        0 as "level"
    FROM
        pg_matviews
    UNION ALL
    SELECT
        child.matviewname,
        parent.level + 1 as "level"
    FROM
        matview_dependencies parent
        JOIN pg_depend ON (parent.matviewname::regclass::oid = pg_depend.refobjid)
        JOIN pg_rewrite ON (pg_depend.objid = pg_rewrite.oid)
        JOIN pg_matviews child ON (pg_rewrite.ev_class = child.matviewname::regclass::oid)
    WHERE parent.matviewname != child.matviewname
)

SELECT
    matviewname
FROM
    matview_dependencies
GROUP BY
    matviewname
ORDER BY
    MAX(level), matviewname
"""


class Command(BaseCommand):
    help = "Refresh all materialized views."

    def handle(self, *args, **kwargs):
        """
        Query the database for all materialized views, sorted topologically
        based on the dependencies between views. Refreshes each view in order,
        then performs a VACUUM ANALYZE to update the database statistics.
        """

        with connection.cursor() as cursor:
            cursor.execute(
                sql.SQL(
                    """
                    SELECT relname as "relation"
                    FROM pg_class LEFT JOIN pg_namespace ON (pg_class.relnamespace = pg_namespace.oid)
                    WHERE nspname = 'public' AND relkind = 'r'
                    """
                )
            )

            # VACUUM FULL aggressively reclaims disk space by rewriting the heap
            # and removing deleted tuples. Requires an exclusive table lock, so only
            # do this on tables that are not direclty used by the application.
            # This is necessary to reduce disk usage when tables are frequently
            # truncated and reimported.
            for (relation,) in cursor.fetchall():
                self.stdout.write("Cleaning table '%s'" % relation)
                _t0 = time()
                cursor.execute(
                    sql.SQL("VACUUM FULL {}").format(sql.Identifier(relation))
                )
                _t1 = time()
                self.stdout.write("Finished cleaning in %.2f seconds" % (_t1 - _t0))

            with transaction.atomic():
                cursor.execute(RECURSIVE_VIEWS_QUERY)

                for (view,) in cursor.fetchall():
                    self.stdout.write("Refreshing materialized view '%s'..." % view)
                    _t0 = time()
                    cursor.execute(
                        sql.SQL("REFRESH MATERIALIZED VIEW CONCURRENTLY {}").format(
                            sql.Identifier(view)
                        )
                    )
                    _t1 = time()
                    self.stdout.write("Refreshed view in %.2f seconds" % (_t1 - _t0))
            self.stdout.write("Updating database statistics...")
            _t0 = time()
            # VACUUM ANALYZE updates PostgreSQL's internal statistics about the database.
            # It also updates the visibility map, allowing for index-only
            # scans in many cases.
            cursor.execute(sql.SQL("VACUUM ANALYZE"))
            _t1 = time()
            self.stdout.write(
                "Updated database statistics in %.2f seconds" % (_t1 - _t0)
            )
