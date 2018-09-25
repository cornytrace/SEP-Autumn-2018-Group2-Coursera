from datetime import timedelta

from django.db.models import Count, Q, Subquery
from django.db.models.functions import Coalesce, Now
from rest_framework import serializers

from coursera.models import (
    Branch,
    Course,
    CourseMembership,
    CourseProgress,
    EITDigitalUser,
    Grade,
    Item,
    Lesson,
    Module,
    PassingState,
)


class CourseAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            "pk",
            "slug",
            "name",
            "level",
            "enrolled_learners",
            "leaving_learners",
            "finished_learners",
            "modules",
            "cohorts",
        ]

    enrolled_learners = serializers.SerializerMethodField()
    leaving_learners = serializers.SerializerMethodField()
    finished_learners = serializers.SerializerMethodField()
    modules = serializers.SerializerMethodField()
    cohorts = serializers.SerializerMethodField()

    def get_enrolled_learners(self, obj):
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
                    .filter(
                        passing_state__description__in=[
                            PassingState.PASSED,
                            PassingState.VERIFIED_PASSED,
                        ]
                    )
                    .values("eitdigital_user_id")
                )
                .difference(
                    CourseProgress.objects.filter(course_id=obj.pk)
                    .filter(timestamp__gt=Now() - timedelta(weeks=6))
                    .values("eitdigital_user_id")
                )
                .count()
            )

    def get_finished_learners(self, obj):
        try:
            return obj.finished_learners
        except AttributeError:
            return Course.objects.filter(pk=obj.pk).aggregate(
                finished_learners=Coalesce(
                    Count(
                        "grades",
                        filter=Q(
                            grades__passing_state__description__in=[
                                PassingState.PASSED,
                                PassingState.VERIFIED_PASSED,
                            ]
                        ),
                    ),
                    0,
                )
            )["finished_learners"]

    def get_modules(self, obj):
        try:
            return obj.modules
        except AttributeError:
            return Branch.objects.filter(
                pk=Subquery(
                    Branch.objects.filter(course_id=obj.pk)
                    .order_by("-authoring_course_branch_created_ts")
                    .values("pk")[:1]
                )
            ).aggregate(modules=Coalesce(Count("modules"), 0))["modules"]

    def get_cohorts(self, obj):
        try:
            return obj.cohorts
        except AttributeError:
            return obj.sessions.count()
