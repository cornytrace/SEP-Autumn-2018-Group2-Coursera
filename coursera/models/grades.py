from django.db import models

__all__ = ["Grade", "PassingState"]


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
