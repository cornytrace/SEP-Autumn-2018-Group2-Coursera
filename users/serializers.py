from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk", "email"]

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_unusable_password()
        user.is_active = True
        user.save(force_insert=True)

        request = self.context["request"]
        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain
        context = {
            "email": user.email,
            "domain": domain,
            "site_name": site_name,
            "user": user,
            "token": default_token_generator.make_token(user),
            "protocol": "https" if request.is_secure() else "http",
        }

        subject = "An account has been created"
        body = loader.render_to_string(
            "registration/password_reset_email.html", context
        )

        email_message = EmailMultiAlternatives(subject, body, to=[user.email])
        email_message.send()

        return user


class PasswordResetSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(trim_whitespace=False)

    def validate_token(self, value):
        if not default_token_generator.check_token(self.instance, value):
            raise serializers.ValidationError("Invalid password reset token.")
        return value

    def validate_password(self, value):
        # validate_password raises a ValidationError when validation fails
        validate_password(value, self.instance)
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save(force_update=True)
        return instance
