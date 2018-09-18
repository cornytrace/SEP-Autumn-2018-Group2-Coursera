import pytest

from courses.models import Course


@pytest.mark.django_db
def test_can_create_course():
    course = Course.objects.create(
        course_id="bmHtyVrIEee3CwoIJ_9DVg",
        course_slug="capstone-recommender-systems",
        course_name="Capstone Recommender Systems",
    )
    assert course.pk is not None, "course has no pk"
    Course.objects.get(pk=course.pk)


@pytest.mark.django_db
@pytest.mark.parametrize("field", ["course_id", "course_slug"])
def test_unique_fields(field):
    assert Course._meta.get_field(field).unique, f"Course.{field} is not unique"


@pytest.mark.django_db
def test_course_str(course):
    assert (
        str(course) == "Capstone Recommender Systems"
    ), "incorrect string representation"
