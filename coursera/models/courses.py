from django.db import models

__all__ = ["Course", "Branch", "ItemProgrammingAssignment", "ItemPeerAssignment"]


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
        max_length=65535,
        blank=True,
        null=True,
        db_column="course_branch_changes_description",
    )
    authoring_course_branch_name = models.CharField(
        max_length=255, blank=True, null=True
    )
    authoring_course_branch_created_ts = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "course_branches"


class ItemProgrammingAssignment(models.Model):
    id = models.CharField(max_length=50, db_column="id", primary_key=True)
    branch = models.ForeignKey(
        "Branch",
        related_name="item_programming_assignments",
        on_delete=models.DO_NOTHING,
        db_column="course_branch_id",
        max_length=50,
        blank=True,
        null=True,
    )
    course_item_id = models.ForeignKey(
        "Item",
        related_name="item_programming_assignments",
        on_delete=models.DO_NOTHING,
        db_column="item_id",
        max_length=50,
        blank=True,
        null=True,
    )
    programming_assignment_id = models.CharField(
        db_column="programming_assignment_id", max_length=50, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "course_branch_item_programming_assignments_view"


class ItemPeerAssignment(models.Model):
    id = models.CharField(max_length=50, db_column="id", primary_key=True)
    branch = models.ForeignKey(
        "Branch",
        related_name="item_peer_assignments",
        on_delete=models.DO_NOTHING,
        db_column="course_branch_id",
        max_length=50,
        blank=True,
        null=True,
    )
    course_item_id = models.ForeignKey(
        "Item",
        related_name="item_peer_assignments",
        on_delete=models.DO_NOTHING,
        db_column="item_id",
        max_length=50,
        blank=True,
        null=True,
    )
    peer_assignment_id = models.CharField(
        db_column="peer_assignment_id", max_length=50, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "course_branch_item_peer_assignments_view"
