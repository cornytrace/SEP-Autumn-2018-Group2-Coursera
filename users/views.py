from django.http import JsonResponse
from oauth2_provider.views import ProtectedResourceView
from rest_framework import decorators, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import PasswordResetSerializer, UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.action == "password_reset":
            return [AllowAny()]
        return super().get_permissions()

    @decorators.action(methods=["put"], detail=True)
    def password_reset(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordResetSerializer(
            user, data=request.data, context={"request": self.request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "password set"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestView(ProtectedResourceView):
    def get(self, request, **kwargs):
        return JsonResponse({"success": "You have a valid access token"})
