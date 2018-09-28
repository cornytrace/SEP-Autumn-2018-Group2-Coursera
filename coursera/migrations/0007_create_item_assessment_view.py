# Generated by Django 2.1.1 on 2018-09-25 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("coursera", "0006_create_course_progress_view")]

    operations = [
        migrations.RunSQL(
            sql=[
                """
                CREATE MATERIALIZED VIEW course_branch_item_assessments_view
                AS
                SELECT
                MD5(MD5(course_item_id) || assessment_id)::varchar(50) as id,
                course_branch_id,
                MD5(MD5(course_branch_id) || course_item_id)::varchar(50) as item_id,
                assessment_id
                FROM
                course_branch_item_assessments;
                """,
                """
                CREATE UNIQUE INDEX ON course_branch_item_assessments_view (id)
                """,
                """
                CREATE INDEX ON course_branch_item_assessments_view (item_id)
                """,
            ],
            reverse_sql="""
            DROP MATERIALIZED VIEW IF EXISTS course_branch_item_assessments_view
            """,
        )
    ]
