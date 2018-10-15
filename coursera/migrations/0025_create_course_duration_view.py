# Generated by Django 2.1.2 on 2018-10-15 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("coursera", "0024_alter_attempts_view")]

    operations = [
        migrations.RunSQL(
            [
                """
                CREATE MATERIALIZED VIEW
                    course_duration_view
                AS
                SELECT DISTINCT
                    MD5(MD5(MD5(course_id) || eitdigital_user_id) || MIN(course_progress_ts))::varchar(50) as id,
                    course_id,
                    eitdigital_user_id,
                    MIN(course_progress_ts) AS course_progress_start_ts,
                    MAX(course_progress_ts) - MIN(course_progress_ts) AS duration
                FROM
                    course_progress_view
                GROUP BY
                    course_id, eitdigital_user_id
                """,
                """
                CREATE UNIQUE INDEX ON course_duration_view (id)
                """,
                """
                CREATE INDEX ON course_duration_view (course_id)
                """,
                """
                CREATE INDEX ON course_duration_view (eitdigital_user_id)
                """,
            ],
            reverse_sql="DROP MATERIALIZED VIEW IF EXISTS course_duration_view",
        )
    ]
