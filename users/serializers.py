from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email"]


class PasswordResetSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField()

    def validate_token(self, value):
        if not default_token_generator.check_token(self.instance, value):
            raise serializers.ValidationError("Invalid password reset token.")
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save(force_update=True)
        return instance
