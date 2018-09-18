from datetime import timedelta

import factory
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.utils.crypto import get_random_string
from factory.django import DjangoModelFactory

from users.models import User


class AccessTokenFactory(DjangoModelFactory):
    class Meta:
        model = "oauth2_provider.AccessToken"

    token = factory.LazyFunction(get_random_string)
    expires = factory.LazyFunction(lambda: timezone.now() + timedelta(days=7))


class UserFactory(DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    first_name = "John"
    last_name = "Doe"
    email = "john.doe@example.com"
    role = User.TEACHER
    password = factory.LazyAttribute(lambda x: make_password("password"))

    is_active = True
    is_staff = False
    is_superuser = False
