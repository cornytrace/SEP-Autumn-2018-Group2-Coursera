from time import time

from django.core.management.base import BaseCommand
from django.db import connection, transaction

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
        with connection.cursor() as cursor:
            with transaction.atomic():
                cursor.execute(RECURSIVE_VIEWS_QUERY)

                for (view,) in cursor.fetchall():
                    self.stdout.write("Refreshing materialized view '%s'..." % view)
                    _t0 = time()
                    cursor.execute(
                        """REFRESH MATERIALIZED VIEW CONCURRENTLY "%s" """ % view
                    )
                    _t1 = time()
                    self.stdout.write("Refreshed view in %.2f seconds" % (_t1 - _t0))
            self.stdout.write("Updating database statistics...")
            _t0 = time()
            cursor.execute("VACUUM ANALYZE")
            _t1 = time()
            self.stdout.write(
                "Updated database statistics in %.2f seconds" % (_t1 - _t0)
            )
