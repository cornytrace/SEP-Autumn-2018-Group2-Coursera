from rest_framework.routers import DefaultRouter

from coursera.views import CourseAnalyticsViewSet

app_name = "coursera-api"

router = DefaultRouter()
router.register("course-analytics", CourseAnalyticsViewSet)
urlpatterns = router.urls
