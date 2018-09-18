from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.template import loader
from rest_framework import serializers

from courses.models import Course
from courses.serializers import CourseSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk", "email", "role", "courses"]

    courses = CourseSerializer(many=True)

    @transaction.atomic()
    def create(self, validated_data):
        courses_data = validated_data.pop("courses", [])
        user = User(**validated_data)
        user.set_unusable_password()
        user.is_active = True
        if user.role == User.ADMIN:
            user.is_staff = True
            user.is_superuser = True
        user.save(force_insert=True)

        courses = []
        for course_data in courses_data:
            course, _ = Course.objects.get_or_create(
                course_id=course_data["course_id"],
                defaults={
                    "course_name": course_data["course_name"],
                    "course_slug": course_data["course_slug"],
                },
            )
            courses.append(course)
        user.courses.set(courses)

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

    @transaction.atomic()
    def update(self, instance, validated_data):
        courses_data = validated_data.pop("courses", [])

        courses = []
        for course_data in courses_data:
            course, _ = Course.objects.get_or_create(
                course_id=course_data["course_id"],
                defaults={
                    "course_name": course_data["course_name"],
                    "course_slug": course_data["course_slug"],
                },
            )
            courses.append(course)
        instance.courses.set(courses)

        if "role" in validated_data and validated_data["role"] == User.ADMIN:
            validated_data.update({"is_staff": True, "is_superuser": True})
        elif "role" in validated_data:
            validated_data.update({"is_staff": False, "is_superuser": False})

        return super().update(instance, validated_data)


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
