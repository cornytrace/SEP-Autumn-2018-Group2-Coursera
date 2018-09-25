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
            name='Branch',
            fields=[
                ('id', models.CharField(db_column='course_branch_id', max_length=50, primary_key=True, serialize=False)),
                ('changes_description', models.CharField(blank=True, db_column='course_branch_changes_description', max_length=65535, null=True)),
                ('authoring_course_branch_name', models.CharField(blank=True, max_length=255, null=True)),
                ('authoring_course_branch_created_ts', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'course_branches',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(blank=True, db_column='course_grade_ts', null=True)),
                ('overall_passed_items', models.IntegerField(blank=True, db_column='course_grade_overall_passed_items', null=True)),
                ('overall', models.FloatField(blank=True, db_column='course_grade_overall', null=True)),
                ('verified_passed_items', models.IntegerField(blank=True, db_column='course_grade_verified_passed_items', null=True)),
                ('verified', models.FloatField(blank=True, db_column='course_grade_verified', null=True)),
            ],
            options={
                'db_table': 'course_grades_view',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.CharField(blank=True, db_column='course_item_id', max_length=255, null=True)),
                ('order', models.IntegerField(blank=True, db_column='course_branch_item_order', null=True)),
                ('type_id', models.IntegerField(blank=True, db_column='course_item_type_id', null=True)),
                ('name', models.CharField(blank=True, db_column='course_branch_item_name', max_length=255, null=True)),
                ('optional', models.BooleanField(blank=True, db_column='course_branch_item_optional', null=True)),
                ('atom_id', models.CharField(blank=True, max_length=255, null=True)),
                ('atom_version_id', models.IntegerField(blank=True, null=True)),
                ('atom_is_frozen', models.BooleanField(blank=True, db_column='course_branch_atom_is_frozen', null=True)),
            ],
            options={
                'db_table': 'course_branch_items',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('lesson_id', models.CharField(blank=True, db_column='course_lesson_id', max_length=50, null=True)),
                ('order', models.IntegerField(blank=True, db_column='course_branch_lesson_order', null=True)),
                ('name', models.CharField(blank=True, db_column='course_branch_lesson_name', max_length=10000, null=True)),
            ],
            options={
                'db_table': 'course_branch_lessons',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('module_id', models.CharField(blank=True, db_column='course_module_id', max_length=50, null=True)),
                ('order', models.IntegerField(blank=True, db_column='course_branch_module_order', null=True)),
                ('name', models.CharField(blank=True, db_column='course_branch_module_name', max_length=2000, null=True)),
                ('description', models.CharField(blank=True, db_column='course_branch_module_desc', max_length=10000, null=True)),
            ],
            options={
                'db_table': 'course_branch_modules_view',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PassingState',
            fields=[
                ('id', models.IntegerField(db_column='course_passing_state_id', primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, choices=[('not passed', 'Not passed'), ('passed', 'Passed'), ('verified passed', 'Verified passed'), ('not passable', 'Not passable')], db_column='course_passing_state_desc', max_length=255, null=True)),
            ],
            options={
                'db_table': 'course_passing_states',
                'managed': False,
            },
        ),
    ]
