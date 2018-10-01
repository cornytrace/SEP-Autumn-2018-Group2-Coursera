from datetime import timedelta

from coursera.models import *
from django.contrib.postgres.fields import JSONField
from django.db.models import (
    Avg,
    Count,
    DateField,
    F,
    Max,
    Min,
    Q,
    Subquery,
    Sum,
    Window,
)
from django.db.models.functions import Cast, Coalesce, TruncMonth
from django.utils.timezone import now
from rest_framework import serializers


class VideoAnalyticsSerializer(serializers.ModelSerializer):
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
            "atom_id",
            "atom_version_id",
            "atom_is_frozen",
            "watched_video",
        ]

    watched_video = serializers.SerializerMethodField()

    def get_watched_video(self, obj):
        try:
            return obj.watchers_for_video
        except AttributeError:
            return (
                ClickstreamEvent.objects.annotate(
                    value_json=Cast("value", output_field=JSONField())
                )
                .filter(
                    course_id=obj.branch_id,
                    value_json__item_id=obj.item_id,
                    key="start",
                )
                .aggregate(watchers_for_video=Coalesce(Count("pk"), -1))[
                    "watchers_for_video"
                ]
            )


class CourseAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            "id",
            "slug",
            "name",
            "level",
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

    def _filter_current_branch(self, course_id):
        """
        Return a filtered queryset with just the current branch for `course_id`.
        """
        return Branch.objects.filter(
            pk=Subquery(
                Branch.objects.filter(course_id=course_id)
                .order_by("-authoring_course_branch_created_ts")
                .values("pk")[:1]
            )
        )

    def get_enrolled_learners(self, obj):
        """
        Return the number of members for `obj` with either a LEARNER
        or PRE_ENROLLED_LEARNER status.
        """
        try:
            return obj.enrolled_learners
        except AttributeError:
            return Course.objects.filter(pk=obj.pk).aggregate(
                enrolled_learners=Coalesce(
                    Count(
                        "course_memberships",
                        filter=Q(
                            course_memberships__role__in=[
                                CourseMembership.LEARNER,
                                CourseMembership.PRE_ENROLLED_LEARNER,
                            ]
                        ),
                    ),
                    0,
                )
            )["enrolled_learners"]

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
        try:
            return obj.finished_learners
        except AttributeError:
            return Course.objects.filter(pk=obj.pk).aggregate(
                finished_learners=Coalesce(
                    Count(
                        "grades",
                        filter=Q(
                            grades__passing_state__in=[
                                Grade.PASSED,
                                Grade.VERIFIED_PASSED,
                            ]
                        ),
                    ),
                    0,
                )
            )["finished_learners"]

    def get_modules(self, obj):
        """
        Return the number of modules for `obj`'s most recent branch.
        """
        try:
            return obj.modules
        except AttributeError:
            return self._filter_current_branch(obj.pk).aggregate(
                modules=Coalesce(Count("modules"), 0)
            )["modules"]

    def get_quizzes(self, obj):
        """
        Return the number of quizzes (assessments) for `obj`'s most recent
        branch.
        """
        try:
            return obj.quizzes
        except AttributeError:
            return self._filter_current_branch(obj.pk).aggregate(
                quizzes=Coalesce(Count("item_assessments"), 0)
            )["quizzes"]

    def get_assignments(self, obj):
        """
        Return the number of peer- and programming assignments for `obj`'s
        most recent branch.
        """
        try:
            return obj.assignments
        except AttributeError:
            return self._filter_current_branch(obj.pk).aggregate(
                assignments=Coalesce(
                    Count("item_programming_assignments")
                    + Count("item_peer_assignments"),
                    0,
                )
            )["assignments"]

    def get_videos(self, obj):
        """
        Return the number of videos (lecture items) for `obj`'s most recent
        branch.
        """
        try:
            return obj.videos
        except AttributeError:
            return self._filter_current_branch(obj.pk).aggregate(
                videos=Coalesce(
                    Count("items", filter=Q(items__type__description=ItemType.LECTURE)),
                    0,
                )
            )["videos"]

    def get_cohorts(self, obj):
        """
        Return the number of cohorts (on-demand sessions) for `obj`.
        """
        try:
            return obj.cohorts
        except AttributeError:
            return obj.sessions.count()

    def get_ratings(self, obj):
        """
        Return the number of ratings for each rating from 1 to 10 for `obj`,
        from either a first-week or end-of-course Net Promotor Score (NPS).
        """
        try:
            return obj.ratings
        except AttributeError:
            ratings = list(
                CourseRating.objects.filter(course_id=obj.pk)
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
                Grade.objects.filter(course_id=obj.pk)
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
        try:
            return obj.average_time
        except AttributeError:
            return (
                obj.progress.values("eitdigital_user_id")
                .annotate(time_spent=Max("timestamp") - Min("timestamp"))
                .aggregate(average_time=Avg("time_spent"))
            )["average_time"]

    def get_average_time_per_module(self, obj):
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
