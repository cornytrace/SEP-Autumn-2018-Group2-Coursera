import factory
from django.conf import settings
from django.contrib.auth.hashers import make_password
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    first_name = "John"
    last_name = "Doe"
    email = "john.doe@example.com"
    password = factory.LazyAttribute(lambda x: make_password("password"))

    is_active = True
    is_staff = False
    is_superuser = False
