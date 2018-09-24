import pytest

from coursera.models import Course
from coursera.serializers import CourseAnalyticsSerializer


@pytest.mark.django_db
def test_serialize_course(coursera_course):
    serializer = CourseAnalyticsSerializer(instance=coursera_course)
    assert serializer.data == {
        "pk": "27_khHs4EeaXRRKK7mMjqw",
        "course_slug": "design-thinking-entrepreneurship",
        "course_name": "Innovation & Entrepreneurship - From Design Thinking to Funding",
        "course_level": Course.INTERMEDIATE,
        "enrolled_learners": 5453,
        "finished_learners": 47,
        "modules": 10,
    }
