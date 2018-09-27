# Generated by Django 2.1.1 on 2018-09-26 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("coursera", "0010_create_feedback_course_rating_view")]

    operations = [
        migrations.RunSQL(
            sql=[
                """
                CREATE MATERIALIZED VIEW IF NOT EXISTS
                    last_activity_view
                AS
                SELECT
                    DISTINCT ON (course_id, eitdigital_user_id)
                    MD5(MD5(MD5(MD5(MD5(course_id) || course_item_id) || eitdigital_user_id) || course_progress_state_type_id) || course_progress_ts)::varchar(50) as id,
                    course_id,
                    MD5(MD5(course_branch_id) || course_item_id)::varchar(50) as item_id,
                    eitdigital_user_id,
                    course_progress_state_type_id,
                    course_progress_ts
                FROM
                    course_progress
                    JOIN course_branches USING (course_id)
                    JOIN course_branch_modules USING (course_branch_id)
                    JOIN course_branch_lessons USING (course_branch_id, course_module_id)
                    JOIN course_branch_items USING (course_branch_id, course_lesson_id, course_item_id)
                ORDER BY
                    course_id,
                    eitdigital_user_id,
                    course_branch_module_order DESC
                """
            ],
            reverse_sql="""
            DROP MATERIALIZED VIEW last_activity_view
            """,
        )
    ]
