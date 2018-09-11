from django.urls import path
from rest_framework.routers import DefaultRouter

from users.views import TestView, UserViewSet

app_name = "users-api"

router = DefaultRouter()
router.register(r"users", UserViewSet)
urlpatterns = router.urls + [path("testview/", TestView.as_view(), name="test-view")]
