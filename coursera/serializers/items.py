from functools import partial

from django.db.models import Count, Q
from django.db.models.functions import Coalesce
from django.utils.functional import cached_property
from rest_framework import serializers

from coursera.filters import ClickstreamEventFilterSet, GenericFilterSet
from coursera.models import (
    ClickstreamEvent,
    DiscussionQuestion,
    Item,
    ItemGrade,
    ItemRating,
)

__all__ = [
    "ItemSerializer",
    "VideoAnalyticsSerializer",
    "AssignmentAnalyticsSerializer",
]


class ItemSerializer(serializers.ModelSerializer):
    """
    Serialize an Item with its basic properties.
    """

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
        ]


class VideoAnalyticsSerializer(ItemSerializer):
    """
    Serializer an Item of type Video with its basic properties
    and calculated analytics.

    Calculates the following analytics:
    
    watched_video: Number of people who started watching the video.
    finished_video: Number of people who finished watching the video.
    video_comments: Number of comments on the video.
    video_likes: Number of likes on the video.
    video_dislikes: Number of dislikes on the video.
    next_item: Next item in the lesson.
    next_video: Next item of type Video in the lesson.
    views_over_runtime: Number of views per 5-second interval in the video.
    """

    class Meta(ItemSerializer.Meta):
        fields = ItemSerializer.Meta.fields + [
            "watched_video",
            "finished_video",
            "video_comments",
            "video_likes",
            "video_dislikes",
            "next_item",
            "next_video",
            "views_over_runtime",
        ]

    watched_video = serializers.SerializerMethodField()
    finished_video = serializers.SerializerMethodField()
    video_comments = serializers.SerializerMethodField()
    video_likes = serializers.SerializerMethodField()
    video_dislikes = serializers.SerializerMethodField()
    next_item = serializers.SerializerMethodField()
    next_video = serializers.SerializerMethodField()
    views_over_runtime = serializers.SerializerMethodField()

    @cached_property
    def filter(self):
        def get_filterset(data=None, queryset=None, *, request=None, prefix=None):
            return GenericFilterSet(data, queryset, request=request, prefix=prefix).qs

        return partial(
            get_filterset, self.context["request"].GET, request=self.context["request"]
        )

    @cached_property
    def clickstream_filter(self):
        def get_filterset(data=None, queryset=None, *, request=None, prefix=None):
            return ClickstreamEventFilterSet(
                data, queryset, request=request, prefix=prefix
            ).qs

        return partial(
            get_filterset, self.context["request"].GET, request=self.context["request"]
        )

    def get_watched_video(self, obj):
        try:
            return obj.watched_video
        except AttributeError:
            return self.clickstream_filter(
                ClickstreamEvent.objects.filter(
                    course_id=obj.branch_id, value__item_id=obj.item_id, key="start"
                )
            ).aggregate(
                watchers_for_video=Coalesce(
                    Count("eitdigital_user_id", distinct=True), 0
                )
            )[
                "watchers_for_video"
            ]

    def get_finished_video(self, obj):
        try:
            return obj.finished_video
        except AttributeError:
            return self.clickstream_filter(
                ClickstreamEvent.objects.filter(
                    course_id=obj.branch_id, value__item_id=obj.item_id, key="end"
                )
            ).aggregate(
                watchers_for_video=Coalesce(
                    Count("eitdigital_user_id", distinct=True), 0
                )
            )[
                "watchers_for_video"
            ]

    def get_video_comments(self, obj):
        try:
            return obj.video_comments
        except AttributeError:
            return self.filter(DiscussionQuestion.objects.filter(item=obj)).aggregate(
                video_comments=Coalesce(Count("pk"), 0)
            )["video_comments"]

    def get_video_likes(self, obj):
        try:
            return obj.video_likes
        except AttributeError:
            return self.filter(
                ItemRating.objects.filter(item=obj, system="LIKE_OR_DISLIKE")
            ).aggregate(video_likes=Coalesce(Count("rating", filter=Q(rating=1)), 0))[
                "video_likes"
            ]

    def get_video_dislikes(self, obj):
        try:
            return obj.video_dislikes
        except AttributeError:
            return self.filter(
                ItemRating.objects.filter(item=obj, system="LIKE_OR_DISLIKE")
            ).aggregate(video_likes=Coalesce(Count("rating", filter=Q(rating=0)), 0))[
                "video_likes"
            ]

    def get_next_item(self, obj):
        try:
            return obj.next_item_id
        except AttributeError:
            try:
                item = Item.objects.get(
                    branch=obj.branch, lesson=obj.lesson, order=obj.order + 1
                )
                if item.type.category == "quiz":
                    passing_fraction = (
                        item.item_grades.aggregate(
                            passing_fraction=Count(
                                "id",
                                filter=Q(
                                    passing_state__in=[
                                        ItemGrade.PASSED,
                                        ItemGrade.VERIFIED_PASSED,
                                    ]
                                ),
                            )
                        )["passing_fraction"]
                        / item.item_grades.aggregate(passing_fraction=Count("id"))[
                            "passing_fraction"
                        ]
                    )
                    return {
                        "item_id": item.item_id,
                        "type": item.type.id,
                        "category": item.type.category,
                        "assessment_id": getattr(
                            item.quizzes.order_by("-version").first(), "base_id", None
                        ),
                        "assessment_version": getattr(
                            item.quizzes.order_by("-version").first(), "version", None
                        ),
                        "passing_fraction": passing_fraction,
                    }
                return {
                    "item_id": item.item_id,
                    "type": item.type.id,
                    "category": item.type.category,
                }
            except Item.DoesNotExist:
                return {"item_id": "", "type": 0, "category": ""}

    def get_next_video(self, obj):
        try:
            return obj.next_video_id
        except AttributeError:
            try:
                item = Item.objects.filter(
                    branch=obj.branch,
                    lesson=obj.lesson,
                    order__gt=obj.order,
                    type__id=1,
                ).order_by("order")[0]
                return {
                    "item_id": item.item_id,
                    "type": item.type.id,
                    "category": item.type.category,
                }
            except IndexError:
                return {"item_id": "", "type": 0, "category": ""}

    def get_views_over_runtime(self, obj):
        try:
            return obj.views_over_runtime
        except AttributeError:
            return list(
                self.clickstream_filter(
                    obj.heartbeats.values_list("timecode")
                    .annotate(count=Count("timecode"))
                    .order_by("timecode")
                )
            )


class AssignmentAnalyticsSerializer(ItemSerializer):
    """
    Serialize an Item of type Assignment with its basic properties
    and calculated analytics.

    Calculates the following analytics:

    submissions: Number of submissions to the assignment.
    submission_ratio: Number of submissions divided by the number of enrolled students.
    average_grade: The average grade of all students who completed the assignment.
    next_item: The next item in the lesson.
    next_assignment: The next item of type Assignment in the lesson.
    """

    class Meta(ItemSerializer.Meta):
        fields = ItemSerializer.Meta.fields + [
            "submissions",
            "submission_ratio",
            "average_grade",
            "next_item",
            "next_assignment",
        ]

    submissions = serializers.IntegerField()
    submission_ratio = serializers.FloatField()
    average_grade = serializers.FloatField()
    next_item = serializers.SerializerMethodField()
    next_assignment = serializers.SerializerMethodField()

    def get_next_item(self, obj):
        try:
            return obj.next_item_id
        except AttributeError:
            try:
                item = Item.objects.get(
                    branch=obj.branch, lesson=obj.lesson, order=obj.order + 1
                )
                return {
                    "item_id": item.item_id,
                    "type": item.type.id,
                    "category": item.type.category,
                }
            except Item.DoesNotExist:
                return {"item_id": "", "type": 0, "category": ""}

    def get_next_assignment(self, obj):
        try:
            return obj.next_video_id
        except AttributeError:
            try:
                item = Item.peer_assignment_objects.filter(
                    branch=obj.branch, lesson=obj.lesson, order__gt=obj.order
                ).order_by("order")[0]
                return {
                    "item_id": item.item_id,
                    "type": item.type.id,
                    "category": item.type.category,
                }
            except IndexError:
                return {"item_id": "", "type": 0, "category": ""}
