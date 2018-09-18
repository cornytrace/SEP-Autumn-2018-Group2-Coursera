import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_can_view_course(admin_api_client, course):
    response = admin_api_client.get(
        reverse("courses-api:course-detail", kwargs={"pk": course.pk})
    )
    assert response.status_code == 200, "could not get course detail"
    assert response.data == {
        "pk": course.pk,
        "course_id": "bmHtyVrIEee3CwoIJ_9DVg",
        "course_slug": "capstone-recommender-systems",
        "course_name": "Capstone Recommender Systems",
    }, "view did not return correct data"
