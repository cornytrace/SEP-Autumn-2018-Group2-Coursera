from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
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
        if self.action == "password_reset" or self.action == "forgot_password":
            return [AllowAny()]
        return super().get_permissions()

    @decorators.action(methods=["put", "post"], detail=True)
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

    @decorators.action(methods=["put", "post"], detail=False)
    def forgot_password(self, request):
        try:
            user = User.objects.get(email=request.data["email"])
            token = default_token_generator.make_token(user)
            link = (
                settings.FRONTEND_URL
                + "resetpassword/"
                + str(token)
                + "/"
                + str(user.pk)
            )
            send_mail(
                "Password Reset Request",
                '<a href="' + link + '"> Click here to reset your password</a>',
                "noreply@" + request.get_host(),
                [user.email],
            )
        except User.DoesNotExist as e:
            pass

        return Response(status=200)


class TestView(ProtectedResourceView):
    def get(self, request, **kwargs):
        return JsonResponse({"success": "You have a valid access token"})
