import json
from urllib.parse import urlparse

import pytest
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from oauth2_provider.models import Application, Grant

from courses.serializers import CourseSerializer
from users.models import User


@pytest.mark.django_db
def test_test_view(user_api_client):
    response = user_api_client.get(reverse("users-api:test-view"))
    assert response.status_code == 200, "could not reach test view"
    assert json.loads(response.content) == {
        "success": "You have a valid access token"
    }, "response returned unexpected data"


@pytest.mark.django_db
def test_test_view_no_access(api_client):
    response = api_client.get(reverse("users-api:test-view"))
    assert response.status_code == 403, "unauthenticated user could reach test view"


@pytest.mark.django_db
def test_login_template(client):
    response = client.get(reverse("users:login"))
    assert "registration/login.html" in [
        t.name for t in response.templates if t.name is not None
    ], "did not use correct template"


@pytest.mark.django_db
def test_user_viewset_me(user_api_client, user):
    response = user_api_client.get(reverse("users-api:user-me"))
    assert response.status_code == 200, "authenticated user could not get data"
    assert response.data["pk"] == user.pk, "data returned to user is not its data"


@pytest.mark.django_db
def test_user_viewset_must_be_admin(user_api_client):
    response = user_api_client.get(reverse("users-api:user-list"))
    assert len(response.data) <= 1, "regular user has permission"


@pytest.mark.django_db
def test_user_viewset_can_get_own_data(user_api_client, user):
    response = user_api_client.get(reverse("users-api:user-list"))
    assert len(response.data) == 1, "regular user cannot access own data"
    assert response.data[0]["pk"] == user.pk, "data returned to user is not its data"


@pytest.mark.django_db
def test_admin_can_access_user_viewset(admin_api_client):
    response = admin_api_client.get(reverse("users-api:user-list"))
    assert response.status_code == 200, "admin user has no permission"


@pytest.mark.django_db
def test_user_viewset_detail(admin_api_client, user):
    response = admin_api_client.get(
        reverse("users-api:user-detail", kwargs={"pk": user.pk})
    )
    assert response.status_code == 200, "admin user can't view user details"
    assert response.data == {
        "pk": user.pk,
        "email": "john.doe@example.com",
        "role": User.TEACHER,
        "courses": [],
    }, "response returned unexpected data"


@pytest.mark.django_db
def test_user_viewset_detail_cannot_get_other_data(user_api_client, user):
    response = user_api_client.get(
        reverse("users-api:user-detail", kwargs={"pk": user.pk + 1})
    )
    assert response.status_code == 403, "regular user can access other users data"


@pytest.mark.django_db
@pytest.mark.parametrize("role", [User.TEACHER, User.QDT])
def test_user_viewset_create(admin_api_client, course, role):
    response = admin_api_client.post(
        reverse("users-api:user-list"),
        {
            "email": "new@example.com",
            "role": role,
            "courses": [CourseSerializer(course).data],
        },
        format="json",
    )
    print(response.content)
    assert response.status_code == 201, "could not create new user"
    assert response.data.keys() == {"pk", "email", "role", "courses"}
    assert (
        response.data.items() >= {"email": "new@example.com", "role": role}.items()
    ), "response returned unexpected data"
    user = User.objects.get(email="new@example.com")
    assert user.role == role, "user role is not f{role}"
    assert user.is_active, "new user is not active"
    assert not user.has_usable_password(), "user password was set"


@pytest.mark.django_db
@pytest.mark.parametrize("role", [User.TEACHER, User.QDT])
def test_user_viewset_user_is_not_a_superuser(admin_api_client, role):
    response = admin_api_client.post(
        reverse("users-api:user-list"), {"email": "new@example.com", "role": role}
    )
    assert response.status_code == 201, "could not create new user"
    user = User.objects.get(pk=response.data["pk"])
    assert user.role == role, f"user is not {role}"
    assert not user.is_staff, f"{role} user is a staff member"
    assert not user.is_superuser, f"{role} user is a superuser"


@pytest.mark.django_db
def test_user_viewset_create_admin(admin_api_client):
    response = admin_api_client.post(
        reverse("users-api:user-list"),
        {"email": "admin2@example.com", "role": User.ADMIN},
    )
    print(response.content)
    assert response.status_code == 201, "could not create new admin user"
    user = User.objects.get(pk=response.data["pk"])
    assert user.role == User.ADMIN, "user is not an admin"
    assert user.is_staff, "admin is not a staff member"
    assert user.is_superuser, "admin is not a superuser"


@pytest.mark.django_db
def test_user_viewset_set_admin_status(admin_api_client, teacher):
    assert teacher.role == User.TEACHER, f"user is not a teacher"
    assert not teacher.is_staff, "user is a staff member"
    assert not teacher.is_superuser, "user is a superuser"

    response = admin_api_client.patch(
        reverse("users-api:user-detail", kwargs={"pk": teacher.pk}),
        {"role": User.ADMIN},
    )
    assert response.status_code == 200, "could not change teacher role to admin"
    admin = User.objects.get(pk=teacher.pk)
    assert admin.role == User.ADMIN, "user is not an admin"
    assert admin.is_staff, "user is not a staff member"
    assert admin.is_superuser, "user is not a superuser"


@pytest.mark.django_db
@pytest.mark.parametrize("role", [User.TEACHER, User.QDT])
def test_user_viewset_remove_admin_status(admin_api_client, admin, role):
    assert admin.role == User.ADMIN, "user is not an admin"
    assert admin.is_staff, "user is not a staff member"
    assert admin.is_superuser, "user is not a superuser"

    response = admin_api_client.patch(
        reverse("users-api:user-detail", kwargs={"pk": admin.pk}), {"role": role}
    )
    assert response.status_code == 200, "could not change admin role to teacher"
    user = User.objects.get(pk=admin.pk)
    assert user.role == role, f"user is not a {role}"
    assert not user.is_staff, "user is a staff member"
    assert not user.is_superuser, "user is a superuser"


@pytest.mark.django_db
def test_user_viewset_update_email(admin_api_client, teacher):
    assert teacher.email != "new@example.com", "email was already set"

    response = admin_api_client.patch(
        reverse("users-api:user-detail", kwargs={"pk": teacher.pk}),
        {"email": "new@example.com"},
    )
    assert response.status_code == 200, "could not change user's email"
    teacher.refresh_from_db()
    assert teacher.email == "new@example.com", "email is not updated"


@pytest.mark.django_db
def test_user_viewset_full_update(admin_api_client, teacher, course):
    assert teacher.role == User.TEACHER, f"user is not a teacher"
    assert not teacher.is_staff, "user is a staff member"
    assert not teacher.is_superuser, "user is a superuser"
    assert teacher.email != "new@example.com", "email was already set"
    assert not teacher.courses.filter(
        course_id=course.course_id
    ).exists(), "course already set"

    response = admin_api_client.put(
        reverse("users-api:user-detail", kwargs={"pk": teacher.pk}),
        {
            "email": "new@example.com",
            "role": User.QDT,
            "courses": [CourseSerializer(course).data],
        },
        format="json",
    )
    assert response.status_code == 200, "could not update user"
    qdt = User.objects.get(pk=teacher.pk)
    assert qdt.role == User.QDT, f"user is not a qdt"
    assert not qdt.is_staff, "user is a staff member"
    assert not qdt.is_superuser, "user is a superuser"
    assert qdt.email == "new@example.com", "email is not updated"
    assert qdt.courses.filter(course_id=course.course_id).exists(), "course not set"


@pytest.mark.django_db
def test_create_user_send_email(admin_api_client, mailoutbox):
    admin_api_client.post(reverse("users-api:user-list"), {"email": "new@example.com"})
    assert len(mailoutbox) == 1, "no mails sent"
    m = mailoutbox[0]
    assert m.subject == "An account has been created", "subject does not match"
    assert list(m.to) == ["new@example.com"], "to address does not match"


@pytest.mark.django_db
def test_reset_password(user, api_client):
    token = default_token_generator.make_token(user)
    response = api_client.put(
        reverse("users-api:user-password-reset", kwargs={"pk": user.pk}),
        {"token": token, "password": "7jz*X6CkMH9s&hEEEF9%QrQ^"},
    )
    assert response.status_code == 200, "could not reset password"
    user.refresh_from_db()
    assert user.check_password(
        "7jz*X6CkMH9s&hEEEF9%QrQ^"
    ), "password was not set correctly"


@pytest.mark.django_db
def test_reset_password_low_quality_password(user, api_client):
    token = default_token_generator.make_token(user)
    response = api_client.put(
        reverse("users-api:user-password-reset", kwargs={"pk": user.pk}),
        {"token": token, "password": "password"},
    )
    assert response.status_code == 400, "request with low-quality password succeeded"
    assert response.data == {
        "password": ["This password is too common."]
    }, "response returned unexpected data"


@pytest.mark.django_db
def test_reset_password_invalid_token(user, api_client):
    response = api_client.put(
        reverse("users-api:user-password-reset", kwargs={"pk": user.pk}),
        {"token": "invalid_token", "password": "new_password"},
    )
    assert response.status_code == 400, "request with invalid token succeeded"
    assert response.data == {
        "token": ["Invalid password reset token."]
    }, "response returned unexpected data"


@pytest.mark.django_db
def test_forgot_password_request(user, api_client, mailoutbox):
    response = api_client.put(
        reverse("users-api:user-forgot-password"), {"email": "john.doe@example.com"}
    )
    assert response.status_code == 200, "response should always return 200"
    assert len(mailoutbox) == 1, "valid password reset request did not send email"


@pytest.mark.django_db
def test_forgot_password_unknown_email(user, api_client, mailoutbox):
    response = api_client.put(
        reverse("users-api:user-forgot-password"), {"email": "jeff.wrong@example.com"}
    )
    assert response.status_code == 200, "response should always return 200"
    assert len(mailoutbox) == 0, "email was sent to an email adress unknown to us"


@pytest.mark.django_db
def test_authorize(api_client, user):
    application = Application.objects.get(name="DASH-IT Frontend")

    response = api_client.post(
        reverse("oauth2_provider:token"),
        {
            "client_id": application.client_id,
            "grant_type": Application.GRANT_PASSWORD,
            "username": user.email,
            "password": "password",
        },
    )
    assert response.status_code == 200, "failed to log in"
    data = json.loads(response.content)
    assert "access_token" in data, "did not recieve access token"
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {data['access_token']}")
    test_response = api_client.get(reverse("users-api:test-view"))
    assert test_response.status_code == 200, "could not access test view"
