# Generated by Django 2.1.1 on 2018-09-25 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("coursera", "0005_create_lessons_items_view")]

    operations = [
        migrations.RunSQL(
            sql=[
                """
                DROP VIEW IF EXISTS course_progress_view
                """,
                """
                CREATE OR REPLACE VIEW course_progress_view
                AS
                SELECT
                MD5(MD5(MD5(MD5(MD5(course_id) || course_item_id) || eitdigital_user_id) || course_progress_state_type_id) || course_progress_ts) as id,
                course_id,
                course_item_id,
                eitdigital_user_id,
                course_progress_state_type_id,
                course_progress_ts
                FROM
                course_progress;
                """,
            ],
            reverse_sql="""
            DROP VIEW course_progress_view
            """,
        )
    ]