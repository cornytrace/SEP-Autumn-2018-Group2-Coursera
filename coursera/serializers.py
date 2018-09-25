from django.db.models import Count, Q, Subquery
from django.db.models.functions import Coalesce
from rest_framework import serializers

from coursera.models import (
    Branch,
    Course,
    CourseMembership,
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
            "finished_learners",
            "modules",
        ]

    enrolled_learners = serializers.SerializerMethodField()
    finished_learners = serializers.SerializerMethodField()
    modules = serializers.SerializerMethodField()

    def get_enrolled_learners(self, obj):
        try:
            return obj.enrolled_learners
        except AttributeError:
            return Course.objects.filter(pk=obj.pk).aggregate(
                enrolled_learners=Coalesce(
                    Count(
                        "course_memberships",
                        filter=Q(course_memberships__role=CourseMembership.LEARNER),
                    ),
                    0,
                )
            )["enrolled_learners"]

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
