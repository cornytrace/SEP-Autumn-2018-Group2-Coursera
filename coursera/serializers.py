from django.db.models import Count, Q, Subquery
from django.db.models.functions import Coalesce
from rest_framework import serializers

from coursera.models import (
    Course,
    CourseBranch,
    CourseBranchModule,
    CourseMembership,
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
            "enrolled_students",
            "modules",
        ]

    enrolled_students = serializers.SerializerMethodField()
    modules = serializers.SerializerMethodField()

    def get_enrolled_students(self, obj):
        try:
            return obj.enrolled_students
        except AttributeError:
            return Course.objects.filter(pk=obj.pk).aggregate(
                enrolled_students=Coalesce(
                    Count(
                        "coursemembership",
                        filter=Q(
                            coursemembership__course_membership_role=CourseMembership.LEARNER
                        ),
                    ),
                    0,
                )
            )["enrolled_students"]

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
