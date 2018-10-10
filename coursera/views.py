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

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.

        Copied and modified from rest_framework.generics.GenericAPIView.
        """
        queryset = self.filter_queryset(self.get_queryset())

        assert "base_id" in self.kwargs and "version" in self.kwargs, (
            "Expected view %s to be called with URL keyword arguments "
            'named "%s" and "%s".' % (self.__class__.__name__, "base_id", "version")
        )

        filter_kwargs = {
            "base_id": self.kwargs["base_id"],
            "version": self.kwargs["version"],
        }
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj
