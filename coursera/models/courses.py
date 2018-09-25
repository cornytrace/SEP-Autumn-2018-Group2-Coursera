from django.db import models

__all__ = [
    "Course",
    "Branch",
    "Module",
    "Grade",
    "CourseMembership",
    "PassingState",
    "EITDigitalUser",
]


class Course(models.Model):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"

    COURSE_LEVELS = (
        (BEGINNER, "Beginner"),
        (INTERMEDIATE, "Intermediate"),
        (ADVANCED, "Advanced"),
    )

    id = models.CharField(primary_key=True, max_length=50, db_column="course_id")
    slug = models.CharField(
        max_length=2000, blank=True, null=True, db_column="course_slug"
    )
    name = models.CharField(
        max_length=2000, blank=True, null=True, db_column="course_name"
    )
    launch_timestamp = models.DateTimeField(
        blank=True, null=True, db_column="course_launch_ts"
    )
    update_timestamp = models.DateTimeField(
        blank=True, null=True, db_column="course_update_ts"
    )
    deleted = models.BooleanField(blank=True, null=True, db_column="course_deleted")
    graded = models.BooleanField(blank=True, null=True, db_column="course_graded")
    description = models.CharField(
        max_length=10000, blank=True, null=True, db_column="course_desc"
    )
    restricted = models.BooleanField(
        blank=True, null=True, db_column="course_restricted"
    )
    verification_enabled_at_timestamp = models.DateTimeField(
        blank=True, null=True, db_column="course_verification_enabled_at_ts"
    )
    primary_translation_equivalent_course_id = models.CharField(
        max_length=50, blank=True, null=True
    )
    preenrollment_timestamp = models.DateTimeField(
        blank=True, null=True, db_column="course_preenrollment_ts"
    )
    workload = models.CharField(
        max_length=100, blank=True, null=True, db_column="course_workload"
    )
    session_enabled_timestamp = models.DateTimeField(
        blank=True, null=True, db_column="course_session_enabled_ts"
    )
    promo_photo_s3_bucket = models.CharField(
        max_length=255, blank=True, null=True, db_column="course_promo_photo_s3_bucket"
    )
    promo_photo_s3_key = models.CharField(
        max_length=10000, blank=True, null=True, db_column="course_promo_photo_s3_key"
    )
    level = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=COURSE_LEVELS,
        db_column="course_level",
    )
    planned_launch_date_text = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="course_planned_launch_date_text",
    )
    header_image_s3_bucket = models.CharField(
        max_length=255, blank=True, null=True, db_column="course_header_image_s3_bucket"
    )
    header_image_s3_key = models.CharField(
        max_length=10000, blank=True, null=True, db_column="course_header_image_s3_key"
    )

    class Meta:
        managed = False
        db_table = "courses"


class EITDigitalUser(models.Model):
    eitdigital_user_id = models.CharField(primary_key=True, max_length=50)
    user_join_ts = models.DateTimeField(blank=True, null=True)
    country_cd = models.CharField(max_length=2, blank=True, null=True)
    region_cd = models.CharField(max_length=3, blank=True, null=True)
    profile_language_cd = models.CharField(max_length=8, blank=True, null=True)
    browser_language_cd = models.CharField(max_length=8, blank=True, null=True)
    reported_or_inferred_gender = models.CharField(max_length=50, blank=True, null=True)
    employment_status = models.CharField(max_length=100, blank=True, null=True)
    educational_attainment = models.CharField(max_length=100, blank=True, null=True)
    student_status = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "users"


class CourseMembership(models.Model):
    PRE_ENROLLED_LEARNER = "PRE_ENROLLED_LEARNER"
    MENTOR = "MENTOR"
    TEACHING_STAFF = "TEACHING_STAFF"
    LEARNER = "LEARNER"
    INSTRUCTOR = "INSTRUCTOR"
    BROWSER = "BROWSER"
    NOT_ENROLLED = "NOT_ENROLLED"

    ROLE_CHOICES = (
        (PRE_ENROLLED_LEARNER, "Pre-enrolled learner"),
        (MENTOR, "Mentor"),
        (TEACHING_STAFF, "Teaching staff"),
        (LEARNER, "Learner"),
        (INSTRUCTOR, "Instructor"),
        (BROWSER, "Browser"),
        (NOT_ENROLLED, "Not enrolled"),
    )

    id = models.CharField(primary_key=True, max_length=50)
    eitdigital_user = models.ForeignKey(
        "EITDigitalUser", related_name="course_memberships", on_delete=models.DO_NOTHING
    )
    course = models.ForeignKey(
        "Course",
        related_name="course_memberships",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    role = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=ROLE_CHOICES,
        db_column="course_membership_role",
    )
    timestamp = models.DateTimeField(
        blank=True, null=True, db_column="course_membership_ts"
    )

    class Meta:
        managed = False
        db_table = "course_memberships_view"
        unique_together = ("eitdigital_user", "course", "timestamp")


class Branch(models.Model):
    id = models.CharField(max_length=50, primary_key=True, db_column="course_branch_id")
    course = models.ForeignKey(
        "Course",
        related_name="branches",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    changes_description = models.CharField(
        max_length=65535, blank=True, null=True, db_column="course_branch_id"
    )
    authoring_course_branch_name = models.CharField(
        max_length=255, blank=True, null=True
    )
    authoring_course_branch_created_ts = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "course_branches"


class Module(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    branch = models.ForeignKey(
        "Branch",
        related_name="modules",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        db_column="course_branch_id",
    )
    module_id = models.CharField(
        max_length=50, blank=True, null=True, db_column="course_module_id"
    )
    order = models.IntegerField(
        blank=True, null=True, db_column="course_branch_module_order"
    )
    name = models.CharField(
        max_length=2000, blank=True, null=True, db_column="course_branch_module_name"
    )
    description = models.CharField(
        max_length=10000, blank=True, null=True, db_column="course_branch_module_desc"
    )

    class Meta:
        managed = False
        db_table = "course_branch_modules_view"
        unique_together = ("branch", "module_id")


class Grade(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    course = models.ForeignKey(
        "Course",
        related_name="grades",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    eitdigital_user = models.ForeignKey(
        "EITDigitalUser", related_name="grades", on_delete=models.DO_NOTHING
    )
    timestamp = models.DateTimeField(blank=True, null=True, db_column="course_grade_ts")
    passing_state = models.ForeignKey(
        "PassingState",
        related_name="grades+",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        db_column="course_passing_state_id",
    )
    overall_passed_items = models.IntegerField(
        blank=True, null=True, db_column="course_grade_overall_passed_items"
    )
    overall = models.FloatField(blank=True, null=True, db_column="course_grade_overall")
    verified_passed_items = models.IntegerField(
        blank=True, null=True, db_column="course_grade_verified_passed_items"
    )
    verified = models.FloatField(
        blank=True, null=True, db_column="course_grade_verified"
    )

    class Meta:
        managed = False
        db_table = "course_grades_view"
        unique_together = ("course", "eitdigital_user", "timestamp")


class PassingState(models.Model):
    NOT_PASSED = "not passed"
    PASSED = "passed"
    VERIFIED_PASSED = "verified passed"
    NOT_PASSABLE = "not passable"

    PASSING_STATES = (
        (NOT_PASSED, "Not passed"),
        (PASSED, "Passed"),
        (VERIFIED_PASSED, "Verified passed"),
        (NOT_PASSABLE, "Not passable"),
    )

    id = models.IntegerField(primary_key=True, db_column="course_passing_state_id")
    description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=PASSING_STATES,
        db_column="course_passing_state_desc",
    )

    class Meta:
        managed = False
        db_table = "course_passing_states"
