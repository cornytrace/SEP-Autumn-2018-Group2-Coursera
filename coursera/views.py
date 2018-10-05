from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from coursera.models import Assessment, ClickstreamEvent, Course, Item
from coursera.serializers import (
    CourseAnalyticsSerializer,
    CourseSerializer,
    QuizAnalyticsSerializer,
    QuizSerializer,
    VideoAnalyticsSerializer,
    VideoSerializer,
)


class CourseAnalyticsViewSet(ReadOnlyModelViewSet):
    queryset = (
        Course.objects.filter_current_branch()
        .with_enrolled_learners()
        # .with_leaving_learners()
        .with_finished_learners()
        .with_modules()
        .with_quizzes()
        .with_assignments()
        .with_videos()
        .with_cohorts()
        .with_average_time()
    )
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseAnalyticsSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        return super().get_queryset().filter(id__in=self.request.user.courses)


class VideoAnalyticsViewSet(ReadOnlyModelViewSet):
    queryset = Item.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]

    lookup_field = "item_id"
    lookup_url_kwarg = "item_id"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return VideoAnalyticsSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(branch__in=self.request.user.courses)
            .filter(branch=self.kwargs["course_id"], type=1)
        )


class QuizAnalyticsViewSet(ReadOnlyModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return QuizAnalyticsSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(item_assessments__branch__in=self.request.user.courses)
            .filter(item_assessments__branch=self.kwargs["course_id"])
        )
