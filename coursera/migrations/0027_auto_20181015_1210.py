# Generated by Django 2.1.2 on 2018-10-15 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("coursera", "0026_create_course_progress_index")]

    operations = [
        migrations.CreateModel(
            name="Attempt",
            fields=[
                (
                    "id",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                ("timestamp", models.DateField()),
            ],
            options={"db_table": "assessment_attempts_view", "managed": False},
        ),
        migrations.CreateModel(
            name="CourseDuration",
            fields=[
                (
                    "id",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                (
                    "timestamp",
                    models.DateTimeField(db_column="course_progress_start_ts"),
                ),
                ("duration", models.DurationField()),
            ],
            options={"db_table": "course_duration_view", "managed": False},
        ),
        migrations.CreateModel(
            name="LastAttempt",
            fields=[
                (
                    "id",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                ("timestamp", models.DateTimeField(db_column="assessment_action_ts")),
                ("score", models.FloatField()),
            ],
            options={"db_table": "assessment_last_attempt_view", "managed": False},
        ),
        migrations.CreateModel(
            name="Response",
            fields=[
                (
                    "id",
                    models.CharField(
                        db_column="assessment_response_id",
                        max_length=50,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "action_id",
                    models.CharField(db_column="assessment_action_id", max_length=50),
                ),
                (
                    "action_version",
                    models.IntegerField(db_column="assessment_action_version"),
                ),
                (
                    "question_id",
                    models.CharField(db_column="assessment_question_id", max_length=50),
                ),
                ("score", models.FloatField(db_column="assessment_response_score")),
                (
                    "weighted_score",
                    models.FloatField(db_column="assessment_response_weighted_score"),
                ),
                ("timestamp", models.DateTimeField(db_column="assessment_action_ts")),
            ],
            options={"db_table": "assessment_response_actions_view", "managed": False},
        ),
        migrations.CreateModel(
            name="ResponseOption",
            fields=[
                (
                    "id",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                (
                    "option_id",
                    models.CharField(db_column="assessment_option_id", max_length=50),
                ),
                (
                    "correct",
                    models.BooleanField(db_column="assessment_response_correct"),
                ),
                (
                    "feedback",
                    models.TextField(db_column="assessment_response_feedback"),
                ),
                (
                    "selected",
                    models.BooleanField(db_column="assessment_response_selected"),
                ),
            ],
            options={"db_table": "assessment_response_options_view", "managed": False},
        ),
        migrations.CreateModel(
            name="Country2To3",
            fields=[
                ("country", models.CharField(max_length=100)),
                (
                    "two_let",
                    models.CharField(max_length=2, primary_key=True, serialize=False),
                ),
                ("three_let", models.CharField(max_length=3)),
            ],
            options={"db_table": "country2to3"},
        ),
        migrations.AlterModelTable(
            name="discussionquestion", table="discussion_questions_view"
        ),
        migrations.AlterModelTable(
            name="itemrating", table="feedback_item_ratings_view"
        ),
    ]
