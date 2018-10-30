from functools import partial

from django.db.models import Avg, Count, DecimalField, FloatField, Max, Min, OuterRef, Q
from django.db.models.functions import Cast, Coalesce
from django.utils.functional import cached_property
from rest_framework import serializers

from coursera.filters import GenericFilterSet
from coursera.models import (
    Attempt,
    DiscussionQuestion,
    Item,
    ItemGrade,
    ItemRating,
    Quiz,
)
from coursera.utils import CountSubquery, NullIf

__all__ = ["QuizSerializer", "QuizAnalyticsSerializer"]


class QuizSerializer(serializers.ModelSerializer):
    """
    Serialize a Quiz with its basic properties.
    """

    class Meta:
        model = Quiz
        fields = [
            "id",
            "base_id",
            "version",
            "name",
            "type",
            "update_timestamp",
            "passing_fraction",
            "graded",
        ]

    name = serializers.CharField()
    graded = serializers.BooleanField()


class QuizAnalyticsSerializer(QuizSerializer):
    """
    Serialize a Quiz with its basic properties
    and calculated statistics.

    Calculates the following statistics:

    average_grade:
        The average grade of all students who completed the quiz.
    grade_distribution:
        The distribution of grades of all students who completed the quiz.
    average_attempts:
        The average number of attempts per student.
    number_of_attempts:
        The distribution of number of attempts per student.
    correct_ratio_per_question:
        The ratio between correct responses and submitted responses per
        question.
    quiz_comments:
        The number of comments on the quiz.
    quiz_likes:
        The number of likes on the quiz.
    quiz_dislikes:
        The number of dislikes on the quiz.
    last_attempt_average_grade:
        The average grade of students' last attempt on the quiz.
    last_attempt_grade_distribution: 
        The distribution of grades of students' last attempt on the quiz.
    next_item:
        The next item in the lesson.
    next_quiz:
        The next item of type Quiz in the lesson.
    """

    class Meta(QuizSerializer.Meta):
        fields = QuizSerializer.Meta.fields + [
            "average_grade",
            "grade_distribution",
            "average_attempts",
            "number_of_attempts",
            "correct_ratio_per_question",
            "quiz_comments",
            "quiz_likes",
            "quiz_dislikes",
            "last_attempt_average_grade",
            "last_attempt_grade_distribution",
            "next_item",
            "next_quiz",
        ]

    average_grade = serializers.FloatField()
    grade_distribution = serializers.SerializerMethodField()
    number_of_attempts = serializers.SerializerMethodField()
    average_attempts = serializers.SerializerMethodField()
    correct_ratio_per_question = serializers.SerializerMethodField()
    quiz_comments = serializers.SerializerMethodField()
    quiz_likes = serializers.SerializerMethodField()
    quiz_dislikes = serializers.SerializerMethodField()
    last_attempt_average_grade = serializers.SerializerMethodField()
    last_attempt_grade_distribution = serializers.SerializerMethodField()
    next_item = serializers.SerializerMethodField()
    next_quiz = serializers.SerializerMethodField()

    @cached_property
    def filter(self):
        """
        Return a partial that applies the GenericFilterSet to the passed
        queryset.

        Requires the request object to be in the context.
        """

        def get_filterset(data=None, queryset=None, *, request=None, prefix=None):
            """
            Apply the GenericFilterSet to the queryset, and return the filtered
            queryset.
            """
            return GenericFilterSet(data, queryset, request=request, prefix=prefix).qs

        return partial(
            get_filterset, self.context["request"].GET, request=self.context["request"]
        )

    def get_grade_distribution(self, obj):
        """
        Return the distribution of grades for this quiz within the given
        timespan.
        """
        return list(
            self.filter(
                ItemGrade.objects.filter(
                    item__quizzes=obj, course=self.context["course_id"]
                )
            )
            .annotate(
                grade=Cast("overall", DecimalField(max_digits=3, decimal_places=2))
            )
            .values_list("grade")
            .order_by("grade")
            .annotate(num_grades=Count("eitdigital_user"))
        )

    def get_average_attempts(self, obj):
        """
        Return the average number of attempts for this quiz within the given
        timespan.
        """
        return (
            self.filter(Attempt.objects.filter(quiz=obj))
            .values("eitdigital_user_id")
            .annotate(number_of_attempts=Count("timestamp"))
            .aggregate(average=Coalesce(Avg("number_of_attempts"), 0))["average"]
        )

    def get_number_of_attempts(self, obj):
        """
        Return the number of users that have used a specific number of attempts
        on the quiz within the given timespan. Every day on which a user
        submitted at least one response is counted as an attempt.
        """
        return list(
            self.filter(Attempt.objects.filter(quiz=obj))
            .annotate(
                number_of_attempts=CountSubquery(
                    GenericFilterSet(
                        self.context["request"].GET,
                        Attempt.objects.filter(
                            quiz_id=OuterRef("quiz_id"),
                            eitdigital_user_id=OuterRef("eitdigital_user_id"),
                        ),
                    ).qs
                )
            )
            .values_list("number_of_attempts")
            .order_by("number_of_attempts")
            .annotate(num_people=Count("number_of_attempts"))
        )

    def get_correct_ratio_per_question(self, obj):
        """
        Return the ratio between the number of correct answers and the total
        number of answers for each question within the given timespan.
        """
        queryset = self.filter(
            obj.answer_count.values_list("question_id").order_by("question_id")
        )
        if "from_date" in self.context["request"].GET:
            return list(
                queryset.annotate(
                    ratio=Cast(
                        Max("count_correct") - Min("count_correct"), FloatField()
                    )
                    / NullIf(
                        Max("count_selected") - Min("count_selected"),
                        0,
                        output_field=FloatField(),
                    )
                )
            )
        return list(
            queryset.annotate(
                ratio=Cast(Max("count_correct"), FloatField())
                / NullIf(Max("count_selected"), 0, output_field=FloatField())
            )
        )

    def get_quiz_comments(self, obj):
        """
        Return the number of comments on this quiz within the given timespan.
        """
        return self.filter(
            DiscussionQuestion.objects.filter(
                item__quizzes=obj, course_id=self.context["course_id"]
            )
        ).aggregate(quiz_comments=Coalesce(Count("pk"), 0))["quiz_comments"]

    def get_quiz_likes(self, obj):
        """
        Return the number of likes on this quiz within the given timespan.
        """
        return self.filter(
            ItemRating.objects.filter(
                item__quizzes=obj,
                course_id=self.context["course_id"],
                system="LIKE_OR_DISLIKE",
            )
        ).aggregate(quiz_likes=Coalesce(Count("rating", filter=Q(rating=1)), 0))[
            "quiz_likes"
        ]

    def get_quiz_dislikes(self, obj):
        """
        Return the number of dislikes on this quiz within the given timespan.
        """
        return self.filter(
            ItemRating.objects.filter(
                item__quizzes=obj,
                course_id=self.context["course_id"],
                system="LIKE_OR_DISLIKE",
            )
        ).aggregate(quiz_dislikes=Coalesce(Count("rating", filter=Q(rating=0)), 0))[
            "quiz_dislikes"
        ]

    def get_last_attempt_average_grade(self, obj):
        """
        Return the average grade of the last attempts for a quiz within the
        given timespan.

        A last attempt is the last submission for each question at a specific
        order in the quiz. If the question at a specific order is replaced,
        and the user submits a response to the new question, the response for
        the new question is counted.
        """
        return self.filter(
            obj.last_attempts.annotate(
                grade=Cast("score", DecimalField(max_digits=3, decimal_places=2))
            )
        ).aggregate(average_grade=Coalesce(Avg("grade"), 0))["average_grade"]

    def get_last_attempt_grade_distribution(self, obj):
        """
        Return the grade distribution of the last attempts for a quiz within
        the given timespan.
        """
        return list(
            self.filter(
                obj.last_attempts.annotate(
                    grade=Cast("score", DecimalField(max_digits=3, decimal_places=2))
                ).values_list("grade")
            ).annotate(count=Count("eitdigital_user_id"))
        )

    def get_next_item(self, obj):
        """
        Return the next item in the lesson, if any.
        """
        try:
            return obj.next_item_id
        except AttributeError:
            try:
                item = Item.objects.get(
                    branch=obj.items.all()[0].branch,
                    lesson=obj.items.all()[0].lesson,
                    order=obj.items.all()[0].order + 1,
                )
                return {
                    "item_id": item.item_id,
                    "type": item.type.id,
                    "category": item.type.category,
                }
            except Item.DoesNotExist:
                return {"item_id": "", "type": 0, "category": ""}

    def get_next_quiz(self, obj):
        """
        Return the next quiz in the lesson, if any.
        """
        try:
            return obj.next_video_id
        except AttributeError:
            try:
                item = Item.objects.filter(
                    branch=obj.items.all()[0].branch,
                    lesson=obj.items.all()[0].lesson,
                    order__gt=obj.items.all()[0].order,
                    type__category="quiz",
                ).order_by("order")[0]
                return {
                    "assessment_id": getattr(
                        item.quizzes.order_by("-version").first(), "base_id", None
                    ),
                    "assessment_version": getattr(
                        item.quizzes.order_by("-version").first(), "version", None
                    ),
                }
            except IndexError:
                return {"assessment_id": "", "assessment_version": 0}
