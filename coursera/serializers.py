from django.db.models import Count, Q, Subquery
from django.db.models.functions import Coalesce
from rest_framework import serializers

from coursera.models import (
    Course,
    CourseBranch,
    CourseBranchModule,
    CourseMembership,
    CoursePassingState,
    EITDigitalUser,
)


class CourseAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            "pk",
            "course_slug",
            "course_name",
            "course_level",
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
                        "coursemembership",
                        filter=Q(
                            coursemembership__course_membership_role=CourseMembership.LEARNER
                        ),
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
                        "coursegrade",
                        filter=Q(
                            coursegrade__course_passing_state__course_passing_state_desc__in=[
                                CoursePassingState.PASSED,
                                CoursePassingState.VERIFIED_PASSED,
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
            return CourseBranch.objects.filter(
                pk=Subquery(
                    CourseBranch.objects.filter(course_id=obj.pk)
                    .order_by("-authoring_course_branch_created_ts")
                    .values("pk")[:1]
                )
            ).aggregate(modules=Coalesce(Count("coursebranchmodule"), 0))["modules"]
