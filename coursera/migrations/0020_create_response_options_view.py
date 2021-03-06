# Generated by Django 2.1.2 on 2018-10-09 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("coursera", "0019_create_assessment_attempts_view")]

    operations = [
        migrations.RunSQL(
            [
                """
                CREATE MATERIALIZED VIEW
                    assessment_response_options_view
                AS
                SELECT
                    MD5(MD5(assessment_response_id) || assessment_option_id)::varchar(50) as id,
                    assessment_response_id,
                    assessment_option_id,
                    assessment_response_correct,
                    assessment_response_feedback,
                    assessment_response_selected
                FROM
                    assessment_response_options
                """,
                """
                CREATE UNIQUE INDEX ON assessment_response_options_view (id)
                """,
                """
                CREATE INDEX ON assessment_response_options_view (assessment_response_id)
                """,
                """
                CREATE INDEX ON assessment_response_options_view (assessment_option_id)
                """,
            ],
            reverse_sql="DROP MATERIALIZED VIEW IF EXISTS assessment_response_options_view",
        )
    ]
