# Generated by Django 2.1.2 on 2018-10-09 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("coursera", "0018_create_assessment_response_view")]

    operations = [
        migrations.RunSQL(
            # Unused, replaced in migration 0024.
            [
                """
                CREATE MATERIALIZED VIEW
                    assessment_attempts_view
                AS
                SELECT
                    MD5(MD5(assessment_id) || eitdigital_user_id)::varchar(50) as id,
                    assessment_id,
                    eitdigital_user_id,
                    COUNT(eitdigital_user_id) / COUNT(DISTINCT assessment_question_id) as number_of_attempts
                FROM
                    assessment_responses
                    JOIN assessment_actions USING (assessment_action_id, assessment_id)
                GROUP BY
                    assessment_id,
                    eitdigital_user_id
                """,
                """
                CREATE UNIQUE INDEX ON assessment_attempts_view (id)
                """,
                """
                CREATE INDEX ON assessment_attempts_view (assessment_id)
                """,
                """
                CREATE INDEX ON assessment_attempts_view (eitdigital_user_id)
                """,
            ],
            reverse_sql="DROP MATERIALIZED VIEW IF EXISTS assessment_attempts_view",
        )
    ]
