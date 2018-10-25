from django.db import models
from django.db.models import OuterRef
from django.db.models.functions import Cast, Coalesce

from coursera.utils import AvgSubquery, CountSubquery

from .grades import ItemGrade

__all__ = [
    "Quiz",
    "AnswerCount",
    "ItemQuiz",
    "Response",
    "Attempt",
    "ResponseOption",
    "LastAttempt",
]


class QuizQuerySet(models.QuerySet):
    def with_average_grade(self, filter):
        subquery = filter(
            ItemGrade.objects.filter(item__quizzes=OuterRef("pk"))
            .annotate(
                grade=Cast(
                    "overall", models.DecimalField(max_digits=3, decimal_places=2)
                )
            )
            .values_list("grade")
        )
        return self.annotate(
            average_grade=Coalesce(AvgSubquery(subquery, db_column="grade"), 0)
        )


class Quiz(models.Model):
    id = models.CharField(max_length=50, primary_key=True, db_column="assessment_id")
    base_id = models.CharField(max_length=50, db_column="assessment_base_id")
    version = models.IntegerField(db_column="assessment_version")
    type = models.CharField(max_length=50, db_column="assessment_type_desc")
    update_timestamp = models.DateTimeField(db_column="assessment_update_ts")
    passing_fraction = models.FloatField(db_column="assessment_passing_fraction")

    items = models.ManyToManyField("Item", through="ItemQuiz", related_name="quizzes")

    objects = QuizQuerySet.as_manager()

    class Meta:
        managed = False
        db_table = "assessments_view"


class ItemQuiz(models.Model):
    id = models.CharField(max_length=50, db_column="id", primary_key=True)
    branch = models.ForeignKey(
        "Branch",
        related_name="item_quizzes",
        on_delete=models.DO_NOTHING,
        db_column="course_branch_id",
        max_length=50,
        blank=True,
        null=True,
    )
    item = models.ForeignKey(
        "Item",
        related_name="item_quizzes",
        on_delete=models.DO_NOTHING,
        db_column="item_id",
        max_length=50,
        blank=True,
        null=True,
    )
    quiz = models.ForeignKey(
        "Quiz",
        related_name="item_quizzes",
        on_delete=models.DO_NOTHING,
        db_column="assessment_id",
        max_length=50,
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "course_branch_item_assessments_view"
        unique_together = ("item", "quiz")


class Response(models.Model):
    id = models.CharField(
        max_length=50, primary_key=True, db_column="assessment_response_id"
    )
    quiz = models.ForeignKey(
        "Quiz",
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


class Attempt(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    quiz = models.ForeignKey(
        "Quiz",
        related_name="attempts",
        on_delete=models.DO_NOTHING,
        db_column="assessment_id",
    )
    eitdigital_user = models.ForeignKey(
        "EITDigitalUser", related_name="attempts", on_delete=models.DO_NOTHING
    )
    timestamp = models.DateField()

    class Meta:
        managed = False
        db_table = "assessment_attempts_view"


class LastAttempt(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    quiz = models.ForeignKey(
        "Quiz",
        related_name="last_attempts",
        on_delete=models.DO_NOTHING,
        db_column="assessment_id",
    )
    eitdigital_user = models.ForeignKey(
        "EITDigitalUser", related_name="last_attempts", on_delete=models.DO_NOTHING
    )
    timestamp = models.DateTimeField(db_column="assessment_action_ts")
    score = models.FloatField()

    class Meta:
        managed = False
        db_table = "assessment_last_attempt_view"


class AnswerCount(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    quiz = models.ForeignKey(
        "Quiz",
        related_name="answer_count",
        on_delete=models.DO_NOTHING,
        db_column="assessment_id",
    )
    question_id = models.CharField(db_column="assessment_question_id", max_length=50)
    timestamp = models.DateField(db_column="assessment_action_ts")
    count_correct = models.IntegerField()
    count_selected = models.IntegerField()

    class Meta:
        managed = False
        db_table = "assessment_answers_over_time_view"
