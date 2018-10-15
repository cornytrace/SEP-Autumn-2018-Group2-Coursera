from django.db import models

__all__ = [
    "CourseDuration",
    "CourseProgress",
    "LastActivity",
    "LastActivityPerModule",
    "ModuleFirstActivity",
    "ModuleLastActivity",
]


class CourseProgress(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    course = models.ForeignKey(
        "Course",
        related_name="progress",
        on_delete=models.DO_NOTHING,
        db_column="course_id",
        max_length=50,
        blank=True,
        null=True,
    )
    item = models.ForeignKey(
        "Item",
        related_name="progress",
        on_delete=models.DO_NOTHING,
        db_column="item_id",
    )
    eitdigital_user = models.ForeignKey(
        "EITDigitalUser",
        related_name="progress",
        on_delete=models.DO_NOTHING,
        db_column="eitdigital_user_id",
    )
    state_type_id = models.IntegerField(
        db_column="course_progress_state_type_id", blank=True, null=True
    )
    timestamp = models.DateTimeField(
        db_column="course_progress_ts", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "course_progress_view"


class CourseDuration(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    course = models.ForeignKey(
        "Course",
        related_name="course_duration",
        on_delete=models.DO_NOTHING,
        db_column="course_id",
        max_length=50,
        blank=True,
        null=True,
    )
    eitdigital_user = models.ForeignKey(
        "EITDigitalUser",
        related_name="course_duration",
        on_delete=models.DO_NOTHING,
        db_column="eitdigital_user_id",
    )
    timestamp = models.DateTimeField(db_column="course_progress_start_ts")
    duration = models.DurationField()

    class Meta:
        managed = False
        db_table = "course_duration_view"


class LastActivity(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    course = models.ForeignKey(
        "Course",
        related_name="last_activity",
        on_delete=models.DO_NOTHING,
        db_column="course_id",
        blank=True,
        null=True,
    )
    item = models.ForeignKey(
        "Item",
        related_name="last_activity",
        on_delete=models.DO_NOTHING,
        db_column="item_id",
        max_length=50,
        blank=True,
        null=True,
    )
    eitdigital_user = models.ForeignKey(
        "EITDigitalUser",
        related_name="last_activity",
        on_delete=models.DO_NOTHING,
        db_column="eitdigital_user_id",
        max_length=50,
        blank=True,
        null=True,
    )
    state_type_id = models.IntegerField(
        db_column="course_progress_state_type_id", blank=True, null=True
    )
    timestamp = models.DateTimeField(
        db_column="course_progress_ts", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "last_activity_view"


class LastActivityPerModule(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    module = models.ForeignKey(
        "Module",
        related_name="last_activity",
        on_delete=models.DO_NOTHING,
        db_column="module_id",
    )
    eitdigital_user = models.ForeignKey(
        "EITDigitalUser",
        related_name="last_activity_per_module",
        on_delete=models.DO_NOTHING,
        db_column="eitdigital_user_id",
    )
    last_activity = models.ForeignKey(
        "LastActivity",
        related_name="last_activity_per_module",
        on_delete=models.DO_NOTHING,
        db_column="last_activity_id",
    )
    timestamp = models.DateTimeField(
        db_column="course_progress_ts", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "last_activity_per_module"


class ModuleLastActivity(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    module = models.ForeignKey(
        "Module",
        related_name="module_last_activity",
        on_delete=models.DO_NOTHING,
        db_column="module_id",
    )
    eitdigital_user = models.ForeignKey(
        "EITDigitalUser",
        related_name="module_last_activity",
        on_delete=models.DO_NOTHING,
        db_column="eitdigital_user_id",
    )
    timestamp = models.DateTimeField(db_column="course_progress_ts")

    class Meta:
        managed = False
        db_table = "module_last_activity_view"


class ModuleFirstActivity(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    module = models.ForeignKey(
        "Module",
        related_name="module_first_activity",
        on_delete=models.DO_NOTHING,
        db_column="module_id",
    )
    eitdigital_user = models.ForeignKey(
        "EITDigitalUser",
        related_name="module_first_activity",
        on_delete=models.DO_NOTHING,
        db_column="eitdigital_user_id",
    )
    timestamp = models.DateTimeField(db_column="course_progress_ts")

    class Meta:
        managed = False
        db_table = "module_first_activity_view"
