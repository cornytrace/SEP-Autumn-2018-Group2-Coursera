# Generated by Django 2.1.1 on 2018-09-20 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "course_id",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                (
                    "course_slug",
                    models.CharField(blank=True, max_length=2000, null=True),
                ),
                (
                    "course_name",
                    models.CharField(blank=True, max_length=2000, null=True),
                ),
                ("course_launch_ts", models.DateTimeField(blank=True, null=True)),
                ("course_update_ts", models.DateTimeField(blank=True, null=True)),
                ("course_deleted", models.BooleanField(blank=True, null=True)),
                ("course_graded", models.BooleanField(blank=True, null=True)),
                (
                    "course_desc",
                    models.CharField(blank=True, max_length=10000, null=True),
                ),
                ("course_restricted", models.BooleanField(blank=True, null=True)),
                (
                    "course_verification_enabled_at_ts",
                    models.DateTimeField(blank=True, null=True),
                ),
                (
                    "primary_translation_equivalent_course_id",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "course_preenrollment_ts",
                    models.DateTimeField(blank=True, null=True),
                ),
                (
                    "course_workload",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "course_session_enabled_ts",
                    models.DateTimeField(blank=True, null=True),
                ),
                (
                    "course_promo_photo_s3_bucket",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "course_promo_photo_s3_key",
                    models.CharField(blank=True, max_length=10000, null=True),
                ),
                (
                    "course_level",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "course_planned_launch_date_text",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "course_header_image_s3_bucket",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "course_header_image_s3_key",
                    models.CharField(blank=True, max_length=10000, null=True),
                ),
            ],
            options={"db_table": "courses", "managed": False},
        ),
        migrations.CreateModel(
            name="CourseMembership",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "course_membership_role",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("course_membership_ts", models.DateTimeField(blank=True, null=True)),
            ],
            options={"db_table": "course_memberships_view", "managed": False},
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "eitdigital_user_id",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                ("user_join_ts", models.DateTimeField(blank=True, null=True)),
                ("country_cd", models.CharField(blank=True, max_length=2, null=True)),
                ("region_cd", models.CharField(blank=True, max_length=3, null=True)),
                (
                    "profile_language_cd",
                    models.CharField(blank=True, max_length=8, null=True),
                ),
                (
                    "browser_language_cd",
                    models.CharField(blank=True, max_length=8, null=True),
                ),
                (
                    "reported_or_inferred_gender",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "employment_status",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "educational_attainment",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "student_status",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
            ],
            options={"db_table": "users", "managed": False},
        ),
        migrations.CreateModel(
            name="CourseBranch",
            fields=[
                (
                    "course_branch_id",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                (
                    "course_branch_changes_description",
                    models.CharField(blank=True, max_length=65535, null=True),
                ),
                (
                    "authoring_course_branch_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "authoring_course_branch_created_ts",
                    models.DateTimeField(blank=True, null=True),
                ),
            ],
            options={"db_table": "course_branches", "managed": False},
        ),
        migrations.CreateModel(
            name="CourseBranchModule",
            fields=[
                (
                    "id",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                (
                    "course_module_id",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "course_branch_module_order",
                    models.IntegerField(blank=True, null=True),
                ),
                (
                    "course_branch_module_name",
                    models.CharField(blank=True, max_length=2000, null=True),
                ),
                (
                    "course_branch_module_desc",
                    models.CharField(blank=True, max_length=10000, null=True),
                ),
            ],
            options={"db_table": "course_branch_modules_view", "managed": False},
        ),
        migrations.CreateModel(
            name="EITDigitalUser",
            fields=[
                (
                    "eitdigital_user_id",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                ("user_join_ts", models.DateTimeField(blank=True, null=True)),
                ("country_cd", models.CharField(blank=True, max_length=2, null=True)),
                ("region_cd", models.CharField(blank=True, max_length=3, null=True)),
                (
                    "profile_language_cd",
                    models.CharField(blank=True, max_length=8, null=True),
                ),
                (
                    "browser_language_cd",
                    models.CharField(blank=True, max_length=8, null=True),
                ),
                (
                    "reported_or_inferred_gender",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "employment_status",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "educational_attainment",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "student_status",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
            ],
            options={"db_table": "users", "managed": False},
        ),
        migrations.CreateModel(
            name="CourseGrade",
            fields=[
                (
                    "id",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                ("course_grade_ts", models.DateTimeField(blank=True, null=True)),
                (
                    "course_grade_overall_passed_items",
                    models.IntegerField(blank=True, null=True),
                ),
                ("course_grade_overall", models.FloatField(blank=True, null=True)),
                (
                    "course_grade_verified_passed_items",
                    models.IntegerField(blank=True, null=True),
                ),
                ("course_grade_verified", models.FloatField(blank=True, null=True)),
            ],
            options={"db_table": "course_grades_view", "managed": False},
        ),
        migrations.CreateModel(
            name="CoursePassingState",
            fields=[
                (
                    "course_passing_state_id",
                    models.IntegerField(primary_key=True, serialize=False),
                ),
                (
                    "course_passing_state_desc",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("not passed", "Not passed"),
                            ("passed", "Passed"),
                            ("verified passed", "Verified passed"),
                            ("not passable", "Not passable"),
                        ],
                        max_length=255,
                        null=True,
                    ),
                ),
            ],
            options={"db_table": "course_passing_states", "managed": False},
        ),
        migrations.CreateModel(
            name="Branch",
            fields=[
                (
                    "id",
                    models.CharField(
                        db_column="course_branch_id",
                        max_length=50,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "changes_description",
                    models.CharField(
                        blank=True,
                        db_column="course_branch_changes_description",
                        max_length=65535,
                        null=True,
                    ),
                ),
                (
                    "authoring_course_branch_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "authoring_course_branch_created_ts",
                    models.DateTimeField(blank=True, null=True),
                ),
            ],
            options={"db_table": "course_branches", "managed": False},
        ),
        migrations.CreateModel(
            name="Grade",
            fields=[
                (
                    "id",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                (
                    "timestamp",
                    models.DateTimeField(
                        blank=True, db_column="course_grade_ts", null=True
                    ),
                ),
                (
                    "overall_passed_items",
                    models.IntegerField(
                        blank=True,
                        db_column="course_grade_overall_passed_items",
                        null=True,
                    ),
                ),
                (
                    "overall",
                    models.FloatField(
                        blank=True, db_column="course_grade_overall", null=True
                    ),
                ),
                (
                    "verified_passed_items",
                    models.IntegerField(
                        blank=True,
                        db_column="course_grade_verified_passed_items",
                        null=True,
                    ),
                ),
                (
                    "verified",
                    models.FloatField(
                        blank=True, db_column="course_grade_verified", null=True
                    ),
                ),
            ],
            options={"db_table": "course_grades_view", "managed": False},
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "item_id",
                    models.CharField(
                        blank=True,
                        db_column="course_item_id",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "order",
                    models.IntegerField(
                        blank=True, db_column="course_branch_item_order", null=True
                    ),
                ),
                (
                    "type_id",
                    models.IntegerField(
                        blank=True, db_column="course_item_type_id", null=True
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        db_column="course_branch_item_name",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "optional",
                    models.BooleanField(
                        blank=True, db_column="course_branch_item_optional", null=True
                    ),
                ),
                ("atom_id", models.CharField(blank=True, max_length=255, null=True)),
                ("atom_version_id", models.IntegerField(blank=True, null=True)),
                (
                    "atom_is_frozen",
                    models.BooleanField(
                        blank=True, db_column="course_branch_atom_is_frozen", null=True
                    ),
                ),
            ],
            options={"db_table": "course_branch_items_view", "managed": False},
        ),
        migrations.CreateModel(
            name="Lesson",
            fields=[
                (
                    "id",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                (
                    "lesson_id",
                    models.CharField(
                        blank=True,
                        db_column="course_lesson_id",
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "order",
                    models.IntegerField(
                        blank=True, db_column="course_branch_lesson_order", null=True
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        db_column="course_branch_lesson_name",
                        max_length=10000,
                        null=True,
                    ),
                ),
            ],
            options={"db_table": "course_branch_lessons_view", "managed": False},
        ),
        migrations.CreateModel(
            name="Module",
            fields=[
                (
                    "id",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                (
                    "module_id",
                    models.CharField(
                        blank=True,
                        db_column="course_module_id",
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "order",
                    models.IntegerField(
                        blank=True, db_column="course_branch_module_order", null=True
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        db_column="course_branch_module_name",
                        max_length=2000,
                        null=True,
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        db_column="course_branch_module_desc",
                        max_length=10000,
                        null=True,
                    ),
                ),
            ],
            options={"db_table": "course_branch_modules_view", "managed": False},
        ),
        migrations.CreateModel(
            name="PassingState",
            fields=[
                (
                    "id",
                    models.IntegerField(
                        db_column="course_passing_state_id",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("not passed", "Not passed"),
                            ("passed", "Passed"),
                            ("verified passed", "Verified passed"),
                            ("not passable", "Not passable"),
                        ],
                        db_column="course_passing_state_desc",
                        max_length=255,
                        null=True,
                    ),
                ),
            ],
            options={"db_table": "course_passing_states", "managed": False},
        ),
        migrations.CreateModel(
            name="CourseProgress",
            fields=[
                ("id", models.TextField(primary_key=True, serialize=False)),
                (
                    "course_id",
                    models.CharField(
                        blank=True, db_column="course_id", max_length=50, null=True
                    ),
                ),
                (
                    "state_type_id",
                    models.IntegerField(
                        blank=True, db_column="course_progress_state_type_id", null=True
                    ),
                ),
                (
                    "timestamp",
                    models.DateTimeField(
                        blank=True, db_column="course_progress_ts", null=True
                    ),
                ),
            ],
            options={"db_table": "course_progress_view", "managed": False},
        ),
        migrations.CreateModel(
            name="OnDemandSession",
            fields=[
                (
                    "id",
                    models.CharField(
                        db_column="on_demand_session_id",
                        max_length=50,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "start_timestamp",
                    models.DateTimeField(
                        blank=True, db_column="on_demand_sessions_start_ts", null=True
                    ),
                ),
                (
                    "end_timestamp",
                    models.DateTimeField(
                        blank=True, db_column="on_demand_sessions_end_ts", null=True
                    ),
                ),
                (
                    "enrollment_end_timestamp",
                    models.DateTimeField(
                        blank=True,
                        db_column="on_demand_sessions_enrollment_end_ts",
                        null=True,
                    ),
                ),
            ],
            options={"db_table": "on_demand_sessions", "managed": False},
        ),
        migrations.CreateModel(
            name="ItemAssessment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "assessment_id",
                    models.CharField(
                        blank=True, db_column="assessment_id", max_length=50, null=True
                    ),
                ),
            ],
            options={
                "db_table": "course_branch_item_assessments_view",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ItemProgrammingAssignment",
            fields=[
                (
                    "id",
                    models.TextField(db_column="id", primary_key=True, serialize=False),
                ),
                (
                    "programming_assignment_id",
                    models.CharField(
                        blank=True,
                        db_column="programming_assignment_id",
                        max_length=50,
                        null=True,
                    ),
                ),
            ],
            options={
                "db_table": "course_branch_item_programming_assignments_view",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ItemPeerAssignment",
            fields=[
                (
                    "id",
                    models.TextField(db_column="id", primary_key=True, serialize=False),
                ),
                (
                    "peer_assignment_id",
                    models.CharField(
                        blank=True,
                        db_column="peer_assignment_id",
                        max_length=50,
                        null=True,
                    ),
                ),
            ],
            options={
                "db_table": "course_branch_item_peer_assignments_view",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="CourseRating",
            fields=[
                (
                    "id",
                    models.TextField(db_column="id", primary_key=True, serialize=False),
                ),
                (
                    "feedback_system",
                    models.CharField(
                        blank=True,
                        db_column="feedback_system",
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "rating",
                    models.IntegerField(
                        blank=True, db_column="feedback_rating", null=True
                    ),
                ),
                (
                    "max_rating",
                    models.IntegerField(
                        blank=True, db_column="feedback_max_rating", null=True
                    ),
                ),
                (
                    "timestamp",
                    models.DateTimeField(
                        blank=True, db_column="feedback_ts", null=True
                    ),
                ),
            ],
            options={"db_table": "feedback_course_ratings_view", "managed": False},
        ),
        migrations.CreateModel(
            name="ItemType",
            fields=[
                (
                    "id",
                    models.IntegerField(
                        db_column="course_item_type_id",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        db_column="course_item_type_desc",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        blank=True,
                        db_column="course_item_type_category",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "graded",
                    models.BooleanField(
                        blank=True, db_column="course_item_type_graded", null=True
                    ),
                ),
                (
                    "atom_content_type_id",
                    models.IntegerField(
                        blank=True, db_column="atom_content_type_id", null=True
                    ),
                ),
            ],
            options={"db_table": "course_item_types", "managed": False},
        ),
        migrations.CreateModel(
            name="LastActivity",
            fields=[
                (
                    "id",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                (
                    "state_type_id",
                    models.IntegerField(
                        blank=True, db_column="course_progress_state_type_id", null=True
                    ),
                ),
                (
                    "timestamp",
                    models.DateTimeField(
                        blank=True, db_column="course_progress_ts", null=True
                    ),
                ),
            ],
            options={"db_table": "last_activity_view", "managed": False},
        ),
        migrations.CreateModel(
            name="LastActivityPerModule",
            fields=[
                (
                    "id",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                (
                    "timestamp",
                    models.DateTimeField(
                        blank=True, db_column="course_progress_ts", null=True
                    ),
                ),
            ],
            options={"db_table": "last_activity_per_module", "managed": False},
        ),
        migrations.CreateModel(
            name="ModuleFirstActivity",
            fields=[
                (
                    "id",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                ("timestamp", models.DateTimeField(db_column="course_progress_ts")),
            ],
            options={"db_table": "module_first_activity_view", "managed": False},
        ),
        migrations.CreateModel(
            name="ModuleLastActivity",
            fields=[
                (
                    "id",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                ("timestamp", models.DateTimeField(db_column="course_progress_ts")),
            ],
            options={"db_table": "module_last_activity_view", "managed": False},
        ),
        migrations.CreateModel(
            name="Assessment",
            fields=[
                (
                    "id",
                    models.CharField(
                        db_column="assessment_id",
                        max_length=50,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "base_id",
                    models.CharField(db_column="assessment_base_id", max_length=50),
                ),
                ("version", models.IntegerField(db_column="assessment_version")),
                (
                    "type",
                    models.CharField(db_column="assessment_type_desc", max_length=50),
                ),
                (
                    "update_timestamp",
                    models.DateTimeField(db_column="assessment_update_ts"),
                ),
                (
                    "passing_fraction",
                    models.FloatField(db_column="assessment_passing_fraction"),
                ),
            ],
            options={"db_table": "assessments_view", "managed": False},
        ),
        migrations.CreateModel(
            name="AssessmentResponses",
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
            ],
            options={"db_table": "assessment_responses_view", "managed": False},
        ),
        migrations.CreateModel(
            name="DiscussionQuestion",
            fields=[
                (
                    "id",
                    models.CharField(
                        db_column="discussion_question_id",
                        max_length=50,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("eitdigital_user_id", models.CharField(max_length=50)),
                (
                    "discussion_question_title",
                    models.CharField(blank=True, max_length=20000, null=True),
                ),
                (
                    "discussion_question_details",
                    models.CharField(blank=True, max_length=20000, null=True),
                ),
                (
                    "discussion_question_context_type",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("course_id", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "course_module_id",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "course_item_id",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "discussion_forum_id",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("country_cd", models.CharField(blank=True, max_length=2, null=True)),
                ("group_id", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "discussion_question_created_ts",
                    models.DateTimeField(blank=True, null=True),
                ),
                (
                    "discussion_question_updated_ts",
                    models.DateTimeField(blank=True, null=True),
                ),
            ],
            options={"db_table": "discussion_questions", "managed": False},
        ),
        migrations.CreateModel(
            name="Heartbeat",
            fields=[
                (
                    "id",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                ("timecode", models.IntegerField()),
            ],
            options={"db_table": "heartbeat_events", "managed": False},
        ),
        migrations.CreateModel(
            name="ItemGrade",
            fields=[
                (
                    "id",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                ("timestamp", models.DateTimeField(db_column="course_item_grade_ts")),
                (
                    "passing_state",
                    models.CharField(
                        choices=[
                            ("not passed", "Not passed"),
                            ("passed", "Passed"),
                            ("verified passed", "Verified passed"),
                        ],
                        db_column="course_item_passing_state_desc",
                        max_length=255,
                    ),
                ),
                ("overall", models.FloatField(db_column="course_item_grade_overall")),
                ("verified", models.FloatField(db_column="course_item_grade_verified")),
                ("pending", models.FloatField(db_column="course_item_grade_pending")),
            ],
            options={"db_table": "course_item_grades_view", "managed": False},
        ),
        migrations.CreateModel(
            name="ItemRating",
            fields=[
                (
                    "id",
                    models.CharField(
                        db_column="course_id",
                        max_length=50,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "course_item_id",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "feedback_unit_id",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "feedback_unit_type",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "feedback_system",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("eitdigital_user_id", models.CharField(max_length=50)),
                ("feedback_rating", models.IntegerField(blank=True, null=True)),
                ("feedback_max_rating", models.IntegerField(blank=True, null=True)),
                (
                    "detailed_context",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("feedback_ts", models.DateTimeField(blank=True, null=True)),
            ],
            options={"db_table": "feedback_item_ratings", "managed": False},
        ),
    ]
