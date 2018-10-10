from django.urls import include, path
from rest_framework.routers import DefaultRouter

from coursera.views import (
    CourseAnalyticsViewSet,
    QuizAnalyticsViewSet,
    VideoAnalyticsViewSet,
)

app_name = "coursera-api"

router = DefaultRouter()
router.register("course-analytics", CourseAnalyticsViewSet)
router.register(
    "video-analytics/(?P<course_id>[-\w]+)", VideoAnalyticsViewSet, base_name="video"
)
urlpatterns = router.urls + [
    path(
        "quiz-analytics/<slug:course_id>/",
        include(
            [
                path(
                    "", QuizAnalyticsViewSet.as_view({"get": "list"}), name="quiz-list"
                ),
                path(
                    "<slug:base_id>/",
                    QuizAnalyticsViewSet.as_view({"get": "list"}),
                    name="quiz-list",
                ),
                path(
                    "<slug:base_id>/<int:version>/",
                    QuizAnalyticsViewSet.as_view({"get": "retrieve"}),
                    name="quiz-detail",
                ),
            ]
        ),
    )
]
