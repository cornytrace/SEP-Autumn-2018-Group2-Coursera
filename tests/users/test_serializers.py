import pytest
from django.contrib.auth.tokens import default_token_generator
from django.core import exceptions
from rest_framework import serializers

from users.serializers import PasswordResetSerializer, UserSerializer


@pytest.mark.django_db
def test_serialize_user(user):
    assert UserSerializer(user).data == {"pk": user.pk, "email": "john.doe@example.com"}


@pytest.mark.django_db
def test_validate_token(user):
    token = default_token_generator.make_token(user)
    serializer = PasswordResetSerializer(instance=user)
    assert serializer.validate_token(token) == token, "token validation failed"
    with pytest.raises(serializers.ValidationError):
        serializer.validate_token("invalid_token")


@pytest.mark.django_db
def test_validate_password(user):
    serializer = PasswordResetSerializer(instance=user)
    assert (
        serializer.validate_password("JzS@*4682JP#%a#uT3QQvndf")
        == "JzS@*4682JP#%a#uT3QQvndf"
    ), "password validation failed"
    with pytest.raises(exceptions.ValidationError):
        serializer.validate_password("password")
    with pytest.raises(exceptions.ValidationError):
        serializer.validate_password("short")
    with pytest.raises(exceptions.ValidationError):
        serializer.validate_password("john.doe@example.org")


@pytest.mark.django_db
def test_update_password(user):
    serializer = PasswordResetSerializer()
    user = serializer.update(user, {"password": "new_password"})
    assert user.check_password("new_password"), "password was not updated"
    user.refresh_from_db()
    assert user.check_password("new_password"), "updated password was not saved"
