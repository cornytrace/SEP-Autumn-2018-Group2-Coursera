from django.db import models

__all__ = ["CourseRating"]


class CourseRating(models.Model):
    NPS_FIRST_WEEK = "NPS_FIRST_WEEK"
    NPS_END_OF_COURSE = "NPS_END_OF_COURSE"
    STAR = "STAR"

    FEEDBACK_SYSTEMS = (
        (NPS_FIRST_WEEK, "First week NPS"),
        (NPS_END_OF_COURSE, "End of course NPS"),
        (STAR, "Star"),
    )

    id = models.TextField(db_column="id", primary_key=True)
    course = models.ForeignKey(
        "Course",
        related_name="course_ratings",
        on_delete=models.DO_NOTHING,
        db_column="course_id",
        max_length=50,
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        "EITDigitalUser",
        related_name="course_ratings",
        on_delete=models.DO_NOTHING,
        db_column="eitdigital_user_id",
        max_length=50,
        blank=True,
        null=True,
    )
    feedback_system = models.CharField(
        db_column="feedback_system",
        max_length=100,
        blank=True,
        null=True,
        choices=FEEDBACK_SYSTEMS,
    )
    rating = models.IntegerField(db_column="feedback_rating", blank=True, null=True)
    max_rating = models.IntegerField(
        db_column="feedback_max_rating", blank=True, null=True
    )
    timestamp = models.DateTimeField(db_column="feedback_ts", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "feedback_course_ratings_view"
        unique_together = ("course", "user", "feedback_system", "timestamp")
