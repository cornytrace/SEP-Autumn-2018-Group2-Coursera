from django.db import models

__all__ = ["Grade", "ItemGrade"]


class Grade(models.Model):
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

    id = models.CharField(primary_key=True, max_length=50)
    course = models.ForeignKey(
        "Course", related_name="grades", on_delete=models.DO_NOTHING
    )
    eitdigital_user = models.ForeignKey(
        "EITDigitalUser", related_name="grades", on_delete=models.DO_NOTHING
    )
    timestamp = models.DateTimeField(db_column="course_grade_ts")
    passing_state = models.CharField(
        max_length=255, choices=PASSING_STATES, db_column="course_passing_state_desc"
    )
    overall_passed_items = models.IntegerField(
        db_column="course_grade_overall_passed_items"
    )
    overall = models.FloatField(db_column="course_grade_overall")
    verified_passed_items = models.IntegerField(
        db_column="course_grade_verified_passed_items"
    )
    verified = models.FloatField(db_column="course_grade_verified")

    class Meta:
        managed = False
        db_table = "course_grades_view"
        unique_together = ("course", "eitdigital_user", "timestamp")


class ItemGrade(models.Model):
    NOT_PASSED = "not passed"
    PASSED = "passed"
    VERIFIED_PASSED = "verified passed"

    PASSING_STATES = (
        (NOT_PASSED, "Not passed"),
        (PASSED, "Passed"),
        (VERIFIED_PASSED, "Verified passed"),
    )

    id = models.CharField(primary_key=True, max_length=50)
    course = models.ForeignKey(
        "Course", related_name="item_grades", on_delete=models.DO_NOTHING
    )
    eitdigital_user = models.ForeignKey(
        "EITDigitalUser", related_name="item_grades", on_delete=models.DO_NOTHING
    )
    item = models.ForeignKey(
        "Item", related_name="item_grades", on_delete=models.DO_NOTHING
    )
    timestamp = models.DateTimeField(db_column="course_item_grade_ts")
    passing_state = models.CharField(
        max_length=255,
        choices=PASSING_STATES,
        db_column="course_item_passing_state_desc",
    )
    overall = models.FloatField(db_column="course_item_grade_overall")
    verified = models.FloatField(db_column="course_item_grade_verified")
    pending = models.FloatField(db_column="course_item_grade_pending")

    class Meta:
        managed = False
        db_table = "course_item_grades_view"
        unique_together = ("course", "item", "eitdigital_user")
