from functools import partial

from django.db.models import F, OuterRef, Subquery
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from coursera.filters import GenericFilterSet
from coursera.models import (Branch, ClickstreamEvent, Course, Item, ItemType,
                             Quiz)
from coursera.serializers import (AssignmentAnalyticsSerializer,
                                  CourseAnalyticsSerializer, CourseSerializer,
                                  ItemSerializer, QuizAnalyticsSerializer,
                                  QuizSerializer, VideoAnalyticsSerializer)


class CourseAnalyticsViewSet(ReadOnlyModelViewSet):
    queryset = Course.objects.filter_current_branch()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    @cached_property
    def generic_filterset(self):
        def get_filterset(data=None, queryset=None, *, request=None, prefix=None):
            return GenericFilterSet(data, queryset, request=request, prefix=prefix).qs

        return partial(get_filterset, self.request.GET, request=self.request)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseAnalyticsSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .filter(id__in=self.request.user.courses)
            .with_enrolled_learners(self.generic_filterset)
            .with_finished_learners(self.generic_filterset)
            .with_paying_learners(self.generic_filterset)
            .annotate(specialization=F("specializations__name"))
            .order_by("specialization", "name")
        )
        if self.action == "retrieve":
            queryset = (
                queryset
                # .with_leaving_learners()
                .with_modules()
                .with_quizzes()
                .with_assignments()
                .with_videos()
                .with_cohorts(self.generic_filterset)
                .with_average_time(self.generic_filterset)
            )
        return queryset


class VideoAnalyticsViewSet(ReadOnlyModelViewSet):
    queryset = Item.objects.filter(type__description=ItemType.LECTURE).filter(
        branch=Subquery(
            Branch.objects.filter(pk=OuterRef("branch_id"))
            .order_by(F("authoring_course_branch_created_ts").desc(nulls_last=True))
            .values("pk")[:1]
        )
    )
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    lookup_field = "item_id"
    lookup_url_kwarg = "item_id"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return VideoAnalyticsSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .filter(branch__course__in=self.request.user.courses)
            .filter(branch__course=self.kwargs["course_id"])
        )
        if self.action == "list":
            queryset = queryset.order_by(
                "lesson__module__order", "lesson__order", "order"
            )
        return queryset


class QuizAnalyticsViewSet(ReadOnlyModelViewSet):
    queryset = Quiz.objects.filter(
        items__branch=Subquery(
            Branch.objects.filter(pk=OuterRef("items__branch_id"))
            .order_by(F("authoring_course_branch_created_ts").desc(nulls_last=True))
            .values("pk")[:1]
        )
    )
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
            .filter(items__branch__course__in=self.request.user.courses)
            .filter(items__branch__course=self.kwargs["course_id"])
            .annotate(name=F("items__name"))
            .annotate(graded=F("items__type__graded"))
        )
        if self.action == "retrieve":
            queryset = queryset.with_average_grade(self.generic_filterset)

        if "base_id" in self.kwargs:
            queryset = queryset.filter(base_id=self.kwargs["base_id"]).order_by(
                "version"
            )
        else:
            queryset = queryset.filter(
                version=Subquery(
                    Quiz.objects.filter(base_id=OuterRef("base_id"))
                    .values("version")
                    .order_by("-version")[:1]
                )
            ).order_by(
                "items__lesson__module__order", "items__lesson__order", "items__order"
            )
        return queryset


class AssignmentAnalyticsViewSet(ReadOnlyModelViewSet):
    queryset = Item.peer_assignment_objects.filter(
        branch=Subquery(
            Branch.objects.filter(pk=OuterRef("branch_id"))
            .order_by(F("authoring_course_branch_created_ts").desc(nulls_last=True))
            .values("pk")[:1]
        )
    )
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    lookup_field = "item_id"
    lookup_url_kwarg = "item_id"

    @cached_property
    def generic_filterset(self):
        def get_filterset(data=None, queryset=None, *, request=None, prefix=None):
            return GenericFilterSet(data, queryset, request=request, prefix=prefix).qs

        return partial(get_filterset, self.request.GET, request=self.request)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AssignmentAnalyticsSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .filter(branch__course__in=self.request.user.courses)
            .filter(branch__course=self.kwargs["course_id"])
        )
        if self.action == "retrieve":
            queryset = (
                queryset.with_submissions(self.generic_filterset)
                .with_submission_ratio(self.generic_filterset)
                .with_average_grade(self.generic_filterset)
            )
        if self.action == "list":
            queryset = queryset.order_by(
                "lesson__module__order", "lesson__order", "order"
            )
        return queryset
