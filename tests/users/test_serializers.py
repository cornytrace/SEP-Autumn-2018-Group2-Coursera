import pytest

from users.serializers import UserSerializer


@pytest.mark.django_db
def test_serialize_user(user):
    assert UserSerializer(user).data == {"pk": user.pk, "email": "john.doe@example.com"}
