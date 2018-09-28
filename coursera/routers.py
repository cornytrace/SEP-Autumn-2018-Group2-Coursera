from rest_framework.routers import DefaultRouter

from coursera.views import CourseAnalyticsViewSet, VideoAnalyticsViewSet

app_name = "coursera-api"

router = DefaultRouter()
router.register("course-analytics", CourseAnalyticsViewSet)
router.register("video-analytics/(?P<course_id>\w+)", VideoAnalyticsViewSet)
urlpatterns = router.urls
