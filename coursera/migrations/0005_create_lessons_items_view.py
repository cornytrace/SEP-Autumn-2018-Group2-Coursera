# Generated by Django 2.1.1 on 2018-09-25 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("coursera", "0004_create_course_grades_view")]

    operations = [
        migrations.RunSQL(
            sql=[
                """
                DROP VIEW IF EXISTS course_branch_items_view
                """,
                """
                CREATE OR REPLACE VIEW course_branch_items_view
                AS
                SELECT
                MD5(MD5(course_branch_id) || course_item_id) as id,
                course_branch_id,
                course_item_id,
                course_lesson_id,
                course_branch_item_order,
                course_item_type_id,
                course_branch_item_name,
                course_branch_item_optional,
                atom_id,
                atom_version_id,
                course_branch_atom_is_frozen
                FROM
                course_branch_items;
                """,
            ],
            reverse_sql="""
            DROP VIEW course_branch_items_view
            """,
        ),
        migrations.RunSQL(
            sql=[
                """
                DROP VIEW IF EXISTS course_branch_lessons_view
                """,
                """
                CREATE OR REPLACE VIEW course_branch_lessons_view
                AS
                SELECT
                MD5(MD5(course_branch_id) || course_lesson_id) as id,
                course_branch_id,
                course_lesson_id,
                course_module_id,
                course_branch_lesson_order,
                course_branch_lesson_name
                FROM
                course_branch_lessons;
                """,
            ],
            reverse_sql="""
            DROP VIEW course_branch_lessons_view
            """,
        ),
    ]
