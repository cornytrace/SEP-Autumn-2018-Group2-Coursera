import pytest

from courses.serializers import CourseSerializer


@pytest.mark.django_db
def test_can_serializer_course(course):
    assert CourseSerializer(course).data == {
        "pk": course.pk,
        "course_id": "bmHtyVrIEee3CwoIJ_9DVg",
        "course_slug": "capstone-recommender-systems",
        "course_name": "Capstone Recommender Systems",
    }
