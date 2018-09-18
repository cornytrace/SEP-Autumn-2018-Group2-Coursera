from django.urls import path
from rest_framework.routers import DefaultRouter

from courses.views import CourseViewSet

app_name = "courses-api"

router = DefaultRouter()
router.register("courses", CourseViewSet)
urlpatterns = router.urls
