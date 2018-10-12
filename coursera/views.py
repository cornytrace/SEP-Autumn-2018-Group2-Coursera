from functools import partial

from django.db.models import F, OuterRef, Subquery
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from coursera.filters import GenericFilterSet
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

    lookup_field = "version"

    @cached_property
    def generic_filterset(self):
        def get_filterset(data=None, queryset=None, *, request=None, prefix=None):
            return GenericFilterSet(data, queryset, request=request, prefix=prefix).qs

        return partial(get_filterset, self.request.GET, request=self.request)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return QuizAnalyticsSerializer
        return super().get_serializer_class()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["course_id"] = self.kwargs["course_id"]
        return context

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .with_average_grade(self.generic_filterset)
            .filter(items__branch__in=self.request.user.courses)
            .filter(items__branch=self.kwargs["course_id"])
            .order_by("base_id", "version")
            .annotate(name=F("items__name"))
        )
        if "base_id" in self.kwargs:
            queryset = queryset.filter(base_id=self.kwargs["base_id"])
        else:
            queryset = queryset.filter(
                version=Subquery(
                    Assessment.objects.filter(base_id=OuterRef("base_id"))
                    .values("version")
                    .order_by("-version")[:1]
                )
            )
        return queryset
