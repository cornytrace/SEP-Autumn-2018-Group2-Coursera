from datetime import date

import pytest
from django.urls import reverse

from coursera.models import Course
from coursera.serializers import CourseAnalyticsSerializer


@pytest.mark.django_db
@pytest.mark.freeze_time("2018-09-25 15:00")
def test_course_analytics_view(teacher_api_client, coursera_course_id):
    response = teacher_api_client.get(
        reverse("coursera-api:course-detail", kwargs={"pk": coursera_course_id})
    )
    assert response.status_code == 200, str(resopnse.content)
    assert response.data == {
        "id": "27_khHs4EeaXRRKK7mMjqw",
        "slug": "design-thinking-entrepreneurship",
        "name": "Innovation & Entrepreneurship - From Design Thinking to Funding",
        "level": Course.INTERMEDIATE,
        "enrolled_learners": 5453,
        "leaving_learners": 5294,
        "finished_learners": 47,
        "modules": 10,
        "quizzes": 27,
        "assignments": 15,
        "videos": 41,
        "cohorts": 46,
        "ratings": [
            (1, 2),
            (2, 0),
            (3, 0),
            (4, 2),
            (5, 4),
            (6, 3),
            (7, 13),
            (8, 24),
            (9, 15),
            (10, 34),
        ],
        "finished_learners_over_time": [
            (date(2017, 2, 1), 0),
            (date(2017, 3, 1), 0),
            (date(2017, 4, 1), 0),
            (date(2017, 5, 1), 5),
            (date(2017, 6, 1), 9),
            (date(2017, 7, 1), 15),
            (date(2017, 8, 1), 15),
            (date(2017, 9, 1), 16),
            (date(2017, 10, 1), 18),
            (date(2017, 11, 1), 21),
            (date(2017, 12, 1), 22),
            (date(2018, 1, 1), 28),
            (date(2018, 2, 1), 32),
            (date(2018, 3, 1), 33),
            (date(2018, 4, 1), 38),
            (date(2018, 5, 1), 41),
            (date(2018, 6, 1), 42),
            (date(2018, 7, 1), 46),
            (date(2018, 8, 1), 47),
        ],
    }
