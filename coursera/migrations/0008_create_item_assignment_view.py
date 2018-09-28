# Generated by Django 2.1.1 on 2018-09-26 07:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("coursera", "0007_create_item_assessment_view")]

    operations = [
        migrations.RunSQL(
            sql=[
                """
                CREATE MATERIALIZED VIEW course_branch_item_programming_assignments_view
                AS
                SELECT
                MD5(MD5(course_item_id) || programming_assignment_id)::varchar(50) as id,
                course_branch_id,
                MD5(MD5(course_branch_id) || course_item_id)::varchar(50) as item_id,
                programming_assignment_id
                FROM
                course_branch_item_programming_assignments
                """,
                """
                CREATE UNIQUE INDEX ON course_branch_item_programming_assignments_view (id)
                """,
                """
                CREATE INDEX ON course_branch_item_programming_assignments_view (item_id)
                """,
            ],
            reverse_sql="""
            DROP MATERIALIZED VIEW IF EXISTS course_branch_item_programming_assignments_view
            """,
        )
    ]
