from django.http import JsonResponse
from oauth2_provider.views import ProtectedResourceView
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class TestView(ProtectedResourceView):
    def get(self, request, **kwargs):
        return JsonResponse({"success": "You have a valid access token"})
