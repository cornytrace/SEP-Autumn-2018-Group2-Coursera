import pytest

from coursera.models import Course
from coursera.serializers import CourseAnalyticsSerializer


@pytest.mark.django_db
def test_serialize_course(coursera_course):
    serializer = CourseAnalyticsSerializer(instance=coursera_course)
    assert serializer.data == {
        "pk": "27_khHs4EeaXRRKK7mMjqw",
        "slug": "design-thinking-entrepreneurship",
        "name": "Innovation & Entrepreneurship - From Design Thinking to Funding",
        "level": Course.INTERMEDIATE,
        "enrolled_learners": 5453,
        "leaving_learners": 5294,
        "finished_learners": 47,
        "modules": 10,
        "cohorts": 46,
    }
