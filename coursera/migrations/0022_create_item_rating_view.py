# Generated by Django 2.1.2 on 2018-10-11 08:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("coursera", "0021_create_discussion_questions_view")]

    operations = [
        migrations.RunSQL(
            [
                """
                CREATE MATERIALIZED VIEW
                    feedback_item_ratings_view
                AS
                SELECT
                    MD5(course_id || course_item_id || feedback_unit_id || feedback_unit_type || feedback_system || eitdigital_user_id || feedback_ts)::varchar(50) as id,
                    course_id,
                    MD5(MD5(course_branch_id) || (
                        SELECT course_item_id
                        FROM course_branch_items bi
                        WHERE bi.course_branch_id = course_branches.course_branch_id
                        AND bi.course_item_id = feedback_item_ratings.course_item_id
                    ))::varchar(50) as item_id,
                    feedback_unit_id,
                    feedback_unit_type,
                    feedback_system,
                    eitdigital_user_id,
                    feedback_rating,
                    feedback_max_rating,
                    detailed_context,
                    feedback_ts
                FROM
                    feedback_item_ratings
                    JOIN course_branches USING (course_id)
                WHERE
                    course_branch_id = (
                        SELECT course_branch_id
                        FROM course_branches cb
                        WHERE course_branches.course_id = cb.course_id
                        ORDER BY authoring_course_branch_created_ts DESC NULLS LAST LIMIT 1
                    )
                """,
                """
                CREATE UNIQUE INDEX ON feedback_item_ratings_view (id)
                """,
                """
                CREATE INDEX ON feedback_item_ratings_view (eitdigital_user_id)
                """,
                """
                CREATE INDEX ON feedback_item_ratings_view (course_id)
                """,
                """
                CREATE INDEX ON feedback_item_ratings_view (item_id)
                """,
            ],
            reverse_sql="DROP MATERIALIZED VIEW IF EXISTS feedback_item_ratings_view",
        )
    ]
