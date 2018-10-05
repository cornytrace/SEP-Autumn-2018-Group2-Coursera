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
router.register(
    "quiz-analytics/(?P<course_id>[-\w]+)", QuizAnalyticsViewSet, base_name="quiz"
)
urlpatterns = router.urls
