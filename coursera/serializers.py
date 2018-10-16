from datetime import timedelta
from functools import partial

from django.contrib.postgres.fields import JSONField
from django.db.models import (Avg, Count, DateField, DecimalField, F,
                              FloatField, Func, Max, Min, OuterRef, Q,
                              Subquery, Sum, Window)
from django.db.models.functions import Cast, Coalesce, TruncMonth
from django.utils.functional import cached_property
from django.utils.timezone import now
from rest_framework import serializers

from coursera.filters import ClickstreamEventFilterSet, GenericFilterSet
from coursera.models import *
from coursera.utils import CountSubquery, NullIf


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            "id",
            "branch",
            "item_id",
            "lesson",
            "order",
            "type",
            "name",
            "optional",
        ]


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "slug", "name", "level"]


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = [
            "id",
            "base_id",
            "version",
            "name",
            "type",
            "update_timestamp",
            "passing_fraction",
        ]

    name = serializers.CharField()


class VideoAnalyticsSerializer(ItemSerializer):
    class Meta(ItemSerializer.Meta):
        fields = ItemSerializer.Meta.fields + [
            "watched_video",
            "finished_video",
            "video_comments",
            "video_likes",
            "video_dislikes",
            "next_item",
            "views_over_runtime",
        ]

    watched_video = serializers.SerializerMethodField()
    finished_video = serializers.SerializerMethodField()
    video_comments = serializers.SerializerMethodField()
    video_likes = serializers.SerializerMethodField()
    video_dislikes = serializers.SerializerMethodField()
    next_item = serializers.SerializerMethodField()
    views_over_runtime = serializers.SerializerMethodField()

    @cached_property
    def filter(self):
        def get_filterset(data=None, queryset=None, *, request=None, prefix=None):
            return GenericFilterSet(data, queryset, request=request, prefix=prefix).qs

        return partial(
            get_filterset, self.context["request"].GET, request=self.context["request"]
        )

    @cached_property
    def clickstream_filter(self):
        def get_filterset(data=None, queryset=None, *, request=None, prefix=None):
            return ClickstreamEventFilterSet(
                data, queryset, request=request, prefix=prefix
            ).qs

        return partial(
            get_filterset, self.context["request"].GET, request=self.context["request"]
        )

    def get_watched_video(self, obj):
        try:
            return obj.watched_video
        except AttributeError:
            return self.clickstream_filter(
                ClickstreamEvent.objects.annotate(
                    value_json=Cast("value", output_field=JSONField())
                ).filter(
                    course_id=obj.branch_id,
                    value_json__item_id=obj.item_id,
                    key="start",
                )
            ).aggregate(watchers_for_video=Coalesce(Count("eitdigital_user_id", distinct=True), 0))[
                "watchers_for_video"
            ]

    def get_finished_video(self, obj):
        try:
            return obj.finished_video
        except AttributeError:
            return self.clickstream_filter(
                ClickstreamEvent.objects.annotate(
                    value_json=Cast("value", output_field=JSONField())
                ).filter(
                    course_id=obj.branch_id, value_json__item_id=obj.item_id, key="end"
                )
            ).aggregate(watchers_for_video=Coalesce(Count("eitdigital_user_id", distinct=True), 0))[
                "watchers_for_video"
            ]

    def get_video_comments(self, obj):
        try:
            return obj.video_comments
        except AttributeError:
            return self.filter(DiscussionQuestion.objects.filter(item=obj)).aggregate(
                video_comments=Coalesce(Count("pk"), 0)
            )["video_comments"]

    def get_video_likes(self, obj):
        try:
            return obj.video_likes
        except AttributeError:
            return self.filter(
                ItemRating.objects.filter(item=obj, system="LIKE_OR_DISLIKE")
            ).aggregate(video_likes=Coalesce(Count("rating", filter=Q(rating=1)), 0))[
                "video_likes"
            ]

    def get_video_dislikes(self, obj):
        try:
            return obj.video_dislikes
        except AttributeError:
            return self.filter(
                ItemRating.objects.filter(item=obj, system="LIKE_OR_DISLIKE")
            ).aggregate(video_likes=Coalesce(Count("rating", filter=Q(rating=0)), 0))[
                "video_likes"
            ]

    def get_next_item(self, obj):
        try:
            return obj.next_item_id
        except AttributeError:
            try:
                item = Item.objects.get(
                    branch=obj.branch, lesson=obj.lesson, order=obj.order + 1
                )
                if item.type.category == "quiz":
                    passing_fraction = (
                        item.item_grades.aggregate(
                            passing_fraction=Count(
                                "id",
                                filter=Q(
                                    passing_state__in=[
                                        ItemGrade.PASSED,
                                        ItemGrade.VERIFIED_PASSED,
                                    ]
                                ),
                            )
                        )["passing_fraction"]
                        / item.item_grades.aggregate(passing_fraction=Count("id"))[
                            "passing_fraction"
                        ]
                    )
                    return {
                        "item_id": item.item_id,
                        "type": item.type.id,
                        "category": item.type.category,
                        "assessment_id": getattr(
                            item.assessments.order_by("-version").first(),
                            "base_id",
                            None,
                        ),
                        "assessment_version": getattr(
                            item.assessments.order_by("-version").first(),
                            "version",
                            None,
                        ),
                        "passing_fraction": passing_fraction,
                    }
                return {
                    "item_id": item.item_id,
                    "type": item.type.id,
                    "category": item.type.category,
                }
            except Item.DoesNotExist:
                return {"item_id": "", "type": 0, "category": ""}

    def get_views_over_runtime(self, obj):
        try:
            return obj.views_over_runtime
        except AttributeError:
            return list(
                self.clickstream_filter(
                    obj.heartbeats.values_list("timecode")
                    .annotate(count=Count("timecode"))
                    .order_by("timecode")
                )
            )


class CourseAnalyticsSerializer(CourseSerializer):
    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + [
            "enrolled_learners",
            "leaving_learners",
            "finished_learners",
            "modules",
            "quizzes",
            "assignments",
            "videos",
            "cohorts",
            "ratings",
            "finished_learners_over_time",
            "leaving_learners_per_module",
            "average_time",
            "average_time_per_module",
            "geo_data",
        ]

    enrolled_learners = serializers.SerializerMethodField()
    leaving_learners = serializers.SerializerMethodField()
    finished_learners = serializers.SerializerMethodField()
    modules = serializers.SerializerMethodField()
    quizzes = serializers.SerializerMethodField()
    assignments = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()
    cohorts = serializers.SerializerMethodField()
    ratings = serializers.SerializerMethodField()
    finished_learners_over_time = serializers.SerializerMethodField()
    leaving_learners_per_module = serializers.SerializerMethodField()
    average_time = serializers.SerializerMethodField()
    average_time_per_module = serializers.SerializerMethodField()
    geo_data = serializers.SerializerMethodField()

    @cached_property
    def filter(self):
        def get_filterset(data=None, queryset=None, *, request=None, prefix=None):
            return GenericFilterSet(data, queryset, request=request, prefix=prefix).qs

        return partial(
            get_filterset, self.context["request"].GET, request=self.context["request"]
        )

    def _filter_current_branch(self, course_id):
        """
        Return a filtered queryset with just the current branch for `course_id`.
        """
        return Branch.objects.filter(
            pk=Subquery(
                Branch.objects.filter(course_id=course_id)
                .order_by(F("authoring_course_branch_created_ts").desc(nulls_last=True))
                .values("pk")[:1]
            )
        )

    def get_enrolled_learners(self, obj):
        """
        Return the number of members for `obj` with either a LEARNER
        or PRE_ENROLLED_LEARNER status.
        """
        return obj.enrolled_learners

    def get_leaving_learners(self, obj):
        """
        Return the number of members for `obj` that have a LEARNER
        or PRE_ENROLLED_LEARNER status, have not finished the course
        and had their last activity more than 6 weeks ago.
        """
        try:
            return obj.leaving_learners
        except AttributeError:
            return (
                CourseMembership.objects.filter(course_id=obj.pk)
                .filter(
                    role__in=[
                        CourseMembership.LEARNER,
                        CourseMembership.PRE_ENROLLED_LEARNER,
                    ]
                )
                .values("eitdigital_user_id")
                .difference(
                    Grade.objects.filter(course_id=obj.pk)
                    .filter(passing_state__in=[Grade.PASSED, Grade.VERIFIED_PASSED])
                    .values("eitdigital_user_id")
                )
                .difference(
                    CourseProgress.objects.filter(course_id=obj.pk)
                    .filter(timestamp__gt=now() - timedelta(weeks=6))
                    .values("eitdigital_user_id")
                )
                .count()
            )

    def get_finished_learners(self, obj):
        """
        Return the number of members for `obj` that have a a passing grade.
        """
        return obj.finished_learners

    def get_modules(self, obj):
        """
        Return the number of modules for `obj`'s most recent branch.
        """
        return obj.modules

    def get_quizzes(self, obj):
        """
        Return the number of quizzes (assessments) for `obj`'s most recent
        branch.
        """
        return obj.quizzes

    def get_assignments(self, obj):
        """
        Return the number of peer- and programming assignments for `obj`'s
        most recent branch.
        """
        return obj.assignments

    def get_videos(self, obj):
        """
        Return the number of videos (lecture items) for `obj`'s most recent
        branch.
        """
        return obj.videos

    def get_cohorts(self, obj):
        """
        Return the number of cohorts (on-demand sessions) for `obj`.
        """
        return obj.cohorts

    def get_ratings(self, obj):
        """
        Return the number of ratings for each rating from 1 to 10 for `obj`,
        from either a first-week or end-of-course Net Promotor Score (NPS).
        """
        try:
            ratings = obj.ratings
        except AttributeError:
            ratings = list(
                self.filter(CourseRating.objects.filter(course_id=obj.pk))
                .filter(
                    feedback_system__in=[
                        CourseRating.NPS_FIRST_WEEK,
                        CourseRating.NPS_END_OF_COURSE,
                    ]
                )
                .values_list("rating")
                .annotate(Count("id"))
                .order_by("rating")
            )
        missing = set(range(1, 11)) - {rating for rating, _ in ratings}
        for i in missing:
            ratings.insert(i - 1, (i, 0))
        return ratings

    def get_finished_learners_over_time(self, obj):
        """
        For each month, show the cumulative number of students that has passed
        the course `obj`.
        """
        try:
            return obj.finished_learners_over_time
        except AttributeError:
            return list(
                self.filter(Grade.objects.filter(course_id=obj.pk))
                .annotate(month=TruncMonth("timestamp", output_field=DateField()))
                .annotate(
                    num_finished=Window(
                        Count(
                            "course_id",
                            filter=Q(
                                passing_state__in=[Grade.PASSED, Grade.VERIFIED_PASSED]
                            ),
                        ),
                        order_by=TruncMonth("timestamp").asc(),
                    )
                )
                .order_by(TruncMonth("timestamp").asc())
                .values_list("month", "num_finished")
                .distinct()
            )

    def get_leaving_learners_per_module(self, obj):
        """
        For each module in course `obj`, get the number of learners who
        haven't passed the course and whose activity furtherst in the course
        was in that module.
        """
        try:
            return obj.leaving_learners_per_module
        except AttributeError:
            return list(
                self._filter_current_branch(obj.pk)
                .get()
                .modules.values_list("module_id")
                .annotate(
                    user_count=Count(
                        "last_activity",
                        filter=Q(
                            last_activity__timestamp__lt=now() - timedelta(weeks=6)
                        ),
                    )
                )
                .order_by("order")
            )

    def get_average_time(self, obj):
        """
        Return the average time that users spend on this course, that is
        the time between the user's first activity and last activity.
        """
        return obj.average_time

    def get_average_time_per_module(self, obj):
        """
        For each module in course `obj`, return the average duration between
        each learners first activity and last activity in that module.
        """
        try:
            return obj.average_time_per_module
        except AttributeError:
            return list(
                self._filter_current_branch(obj.pk)
                .get()
                .modules.values_list("module_id")
                .filter(
                    module_last_activity__eitdigital_user_id=F(
                        "module_first_activity__eitdigital_user_id"
                    )
                )
                .annotate(
                    average_time=Avg(
                        F("module_last_activity__timestamp")
                        - F("module_first_activity__timestamp")
                    )
                )
                .order_by("order")
            )

    def get_geo_data(self, obj):
        """
        Return the count of countries of users of the course.
        """
        try:
            return obj.geo_data
        except AttributeError:
            return list(
                EITDigitalUser.objects.filter(
                    eitdigital_user_id__in=CourseMembership.objects.filter(
                        course_id=obj.pk
                    )
                    .filter(
                        role__in=[
                            CourseMembership.LEARNER,
                            CourseMembership.PRE_ENROLLED_LEARNER,
                        ]
                    )
                    .values("eitdigital_user_id")
                )
                .annotate(three_let=F("country_cd__three_let"))
                .annotate(country_name=F("country_cd__country"))
                .values_list("three_let", "country_name")
                .annotate(country_count=Count("eitdigital_user_id"))
            )


class QuizAnalyticsSerializer(QuizSerializer):
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

    @cached_property
    def filter(self):
        def get_filterset(data=None, queryset=None, *, request=None, prefix=None):
            return GenericFilterSet(data, queryset, request=request, prefix=prefix).qs

        return partial(
            get_filterset, self.context["request"].GET, request=self.context["request"]
        )

    def get_grade_distribution(self, obj):
        return list(
            self.filter(
                ItemGrade.objects.filter(
                    item__assessments=obj, course=self.context["course_id"]
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
        return (
            self.filter(Attempt.objects.filter(assessment=obj))
            .values("eitdigital_user_id")
            .annotate(number_of_attempts=Count("timestamp"))
            .aggregate(average=Coalesce(Avg("number_of_attempts"), 0))["average"]
        )

    def get_number_of_attempts(self, obj):
        """
        Return the number of users that have used a specific number of attempts
        on the quiz. Every day on which a user submitted at least one response
        is counted as an attempt.
        """
        return list(
            self.filter(Attempt.objects.filter(assessment=obj))
            .annotate(
                number_of_attempts=CountSubquery(
                    GenericFilterSet(
                        self.context["request"].GET,
                        Attempt.objects.filter(
                            assessment_id=OuterRef("assessment_id"),
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
        queryset = self.filter(obj.answer_count.values_list("question_id").order_by('question_id'))
        if "from_date" in self.context["request"].GET:
            return list(
                queryset.annotate(
                    ratio=Cast(
                        Max("count_correct") - Min("count_correct"), FloatField()
                    )
                    / NullIf(Max("count_selected") - Min("count_selected"), 0, output_field=FloatField())
                )
            )
        return list(
            queryset.annotate(
                ratio=Cast(Max("count_correct"), FloatField()) / NullIf(Max("count_selected"), 0, output_field=FloatField())
            )
        )

    def get_quiz_comments(self, obj):
        return self.filter(
            DiscussionQuestion.objects.filter(
                item__assessments=obj, course_id=self.context["course_id"]
            )
        ).aggregate(quiz_comments=Coalesce(Count("pk"), 0))["quiz_comments"]

    def get_quiz_likes(self, obj):
        return self.filter(
            ItemRating.objects.filter(
                item__assessments=obj,
                course_id=self.context["course_id"],
                system="LIKE_OR_DISLIKE",
            )
        ).aggregate(quiz_likes=Coalesce(Count("rating", filter=Q(rating=1)), 0))[
            "quiz_likes"
        ]

    def get_quiz_dislikes(self, obj):
        return self.filter(
            ItemRating.objects.filter(
                item__assessments=obj,
                course_id=self.context["course_id"],
                system="LIKE_OR_DISLIKE",
            )
        ).aggregate(quiz_dislikes=Coalesce(Count("rating", filter=Q(rating=0)), 0))[
            "quiz_dislikes"
        ]

    def get_last_attempt_average_grade(self, obj):
        """
        Return the average grade of the last attempts for a quiz.

        A last attempt is the last submission for each question at a specific order
        in the quiz. If the question at a specific order is replaced, and the user
        submits a response to the new question, the response for the new question
        is counted.
        """
        return self.filter(
            obj.last_attempts.annotate(
                grade=Cast("score", DecimalField(max_digits=3, decimal_places=2))
            )
        ).aggregate(average_grade=Coalesce(Avg("grade"), 0))["average_grade"]

    def get_last_attempt_grade_distribution(self, obj):
        return list(
            self.filter(
                obj.last_attempts.annotate(
                    grade=Cast("score", DecimalField(max_digits=3, decimal_places=2))
                ).values_list("grade")
            ).annotate(count=Count("eitdigital_user_id"))
        )

class AssignmentAnalyticsSerializer(ItemSerializer):
    class Meta(ItemSerializer.Meta):
        fields = ItemSerializer.Meta.fields + [
            "submissions",
            "submission_ratio",
            "average_grade",
        ]

    submissions = serializers.SerializerMethodField()
    submission_ratio = serializers.SerializerMethodField()
    average_grade = serializers.SerializerMethodField()

    def get_submissions(self, obj):
        return obj.submissions

    def get_submission_ratio(self, obj):
        return obj.submission_ratio

    def get_average_grade(self, obj):
        return obj.average_grade
