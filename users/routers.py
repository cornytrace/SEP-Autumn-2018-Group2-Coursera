from rest_framework.routers import DefaultRouter

from users.views import UserViewSet

app_name = "users-api"

router = DefaultRouter()
router.register(r"users", UserViewSet)
urlpatterns = router.urls
