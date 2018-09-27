from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ReadOnlyModelViewSet

from coursera.models import Course
from coursera.serializers import CourseAnalyticsSerializer


class CourseAnalyticsViewSet(ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseAnalyticsSerializer

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                id__in=list(
                    self.request.user.courses.values_list("course_id", flat=True)
                )
            )
        )
