from django.db import models
from django.db.models import OuterRef
from django.db.models.functions import Cast

from coursera.utils import AvgSubquery, CountSubquery

from .grades import ItemGrade

__all__ = [
    "Assessment",
    "ItemAssessment",
    "Response",
    "AttemptCount",
    "ResponseOption",
    "LastAttempt",
]


class AssessmentQuerySet(models.QuerySet):
    def with_average_grade(self):
        return self.annotate(
            average_grade=AvgSubquery(
                ItemGrade.objects.filter(item__assessments=OuterRef("pk"))
                .annotate(
                    grade=Cast(
                        "overall", models.DecimalField(max_digits=3, decimal_places=2)
                    )
                )
                .values_list("grade"),
                db_column="grade",
            )
        )


class Assessment(models.Model):
    id = models.CharField(max_length=50, primary_key=True, db_column="assessment_id")
    base_id = models.CharField(max_length=50, db_column="assessment_base_id")
    version = models.IntegerField(db_column="assessment_version")
    type = models.CharField(max_length=50, db_column="assessment_type_desc")
    update_timestamp = models.DateTimeField(db_column="assessment_update_ts")
    passing_fraction = models.FloatField(db_column="assessment_passing_fraction")

    items = models.ManyToManyField(
        "Item", through="ItemAssessment", related_name="assessments"
    )

    objects = AssessmentQuerySet.as_manager()

    class Meta:
        managed = False
        db_table = "assessments_view"


class ItemAssessment(models.Model):
    id = models.CharField(max_length=50, db_column="id", primary_key=True)
    branch = models.ForeignKey(
        "Branch",
        related_name="item_assessments",
        on_delete=models.DO_NOTHING,
        db_column="course_branch_id",
        max_length=50,
        blank=True,
        null=True,
    )
    item = models.ForeignKey(
        "Item",
        related_name="item_assessments",
        on_delete=models.DO_NOTHING,
        db_column="item_id",
        max_length=50,
        blank=True,
        null=True,
    )
    assessment = models.ForeignKey(
        "Assessment",
        related_name="item_assessments",
        on_delete=models.DO_NOTHING,
        db_column="assessment_id",
        max_length=50,
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "course_branch_item_assessments_view"
        unique_together = ("item", "assessment")


class Response(models.Model):
    id = models.CharField(
        max_length=50, primary_key=True, db_column="assessment_response_id"
    )
    assessment = models.ForeignKey(
        "Assessment",
        related_name="responses",
        on_delete=models.DO_NOTHING,
        db_column="assessment_id",
    )
    action_id = models.CharField(db_column="assessment_action_id", max_length=50)
    action_version = models.IntegerField(db_column="assessment_action_version")
    question_id = models.CharField(db_column="assessment_question_id", max_length=50)
    score = models.FloatField(db_column="assessment_response_score")
    weighted_score = models.FloatField(db_column="assessment_response_weighted_score")
    timestamp = models.DateTimeField(db_column="assessment_action_ts")

    class Meta:
        managed = False
        db_table = "assessment_response_actions_view"


class ResponseOption(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    response = models.ForeignKey(
        "Response",
        related_name="response_options",
        on_delete=models.DO_NOTHING,
        db_column="assessment_response_id",
    )
    option_id = models.CharField(max_length=50, db_column="assessment_option_id")
    correct = models.BooleanField(db_column="assessment_response_correct")
    feedback = models.TextField(db_column="assessment_response_feedback")
    selected = models.BooleanField(db_column="assessment_response_selected")

    class Meta:
        managed = False
        db_table = "assessment_response_options_view"


class AttemptCount(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    assessment = models.ForeignKey(
        "Assessment", related_name="attempts", on_delete=models.DO_NOTHING
    )
    eitdigital_user = models.ForeignKey(
        "EITDigitalUser", related_name="attempts", on_delete=models.DO_NOTHING
    )
    number_of_attempts = models.IntegerField()

    class Meta:
        managed = False
        db_table = "assessment_attempts_view"


class LastAttempt(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    assessment = models.ForeignKey(
        "Assessment", related_name="last_attempts", on_delete=models.DO_NOTHING
    )
    eitdigital_user = models.ForeignKey(
        "EITDigitalUser", related_name="last_attempts", on_delete=models.DO_NOTHING
    )
    timestamp = models.DateTimeField(db_column="assessment_action_ts")
    score = models.FloatField()

    class Meta:
        managed = False
        db_table = "assessment_last_attempt_view"
