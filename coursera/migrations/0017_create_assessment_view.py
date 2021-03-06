# Generated by Django 2.1.2 on 2018-10-05 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("coursera", "0016_create_item_grades_view")]

    operations = [
        migrations.RunSQL(
            [
                """
                CREATE MATERIALIZED VIEW
                    assessments_view
                AS
                SELECT
                    assessment_id,
                    assessment_base_id,
                    assessment_version,
                    assessment_type_desc,
                    assessment_update_ts,
                    assessment_passing_fraction
                FROM
                    assessments
                    JOIN assessment_types USING (assessment_type_id)
                """,
                """
                CREATE UNIQUE INDEX ON assessments_view (assessment_id)
                """,
                """
                CREATE INDEX ON assessments_view (assessment_base_id, assessment_version)
                """,
                """
                CREATE INDEX ON assessments_view (assessment_type_desc)
                """,
            ],
            reverse_sql="DROP MATERIALIZED VIEW IF EXISTS assessments_view",
        )
    ]
