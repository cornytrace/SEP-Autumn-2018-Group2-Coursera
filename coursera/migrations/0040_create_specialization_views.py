# Generated by Django 2.1.2 on 2018-10-23 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("coursera", "0039_create_user_payments_view")]

    operations = [
        migrations.RunSQL(
            [
                """
                CREATE MATERIALIZED VIEW
                    specializations_view
                AS
                SELECT
                    specialization_id,
                    specialization_slug,
                    specialization_name,
                    specialization_display_page_launch_ts,
                    sequence_branch_id,
                    specialization_version,
                    base_specialization_id,
                    specialization_primary_domain,
                    specialization_primary_subdomain
                FROM
                    specializations
                """,
                """
                CREATE UNIQUE INDEX ON specializations_view (specialization_id)
                """,
            ],
            reverse_sql="DROP MATERIALIZED VIEW IF EXISTS specializations_view",
        ),
        migrations.RunSQL(
            [
                """
                CREATE MATERIALIZED VIEW
                    specializations_courses_view
                AS
                SELECT
                    MD5(MD5(course_id) || specialization_id)::varchar(50) as id,
                    course_id,
                    specialization_id,
                    current_dt
                FROM
                    specializations_courses_view
                """,
                """
                CREATE UNIQUE INDEX ON specializations_courses_view (id)
                """,
                """
                CREATE INDEX ON specializations_courses_view (course_id)
                """,
                """
                CREATE INDEX ON specializations_courses_view (specialization_id)
                """,
            ],
            reverse_sql="DROP MATERIALIZED VIEW IF EXISTS specializations_courses_view",
        ),
    ]
