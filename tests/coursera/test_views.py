from datetime import date, timedelta

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
    assert response.status_code == 200, str(response.content)
    data = {
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
        "leaving_learners_per_module": [
            ("sGiw3", 1337),
            ("mtiDN", 353),
            ("uNiMX", 302),
            ("Cnbc7", 110),
            ("Q5WbI", 60),
            ("rXWW5", 72),
            ("1TPfk", 40),
            ("j2R4F", 29),
            ("wIGCQ", 99),
            ("DPfkU", 263),
        ],
        "average_time": timedelta(
            days=20, hours=20, minutes=5, seconds=9, microseconds=461960
        ),
        "average_time_per_module": [
            ("sGiw3", timedelta(days=13, seconds=67594, microseconds=396139)),
            ("mtiDN", timedelta(days=12, seconds=33541, microseconds=27827)),
            ("uNiMX", timedelta(days=18, seconds=44361, microseconds=173885)),
            ("Cnbc7", timedelta(days=16, seconds=35902, microseconds=668189)),
            ("Q5WbI", timedelta(days=18, seconds=23504, microseconds=143258)),
            ("rXWW5", timedelta(days=16, seconds=62370, microseconds=129438)),
            ("1TPfk", timedelta(days=10, seconds=69910, microseconds=959793)),
            ("j2R4F", timedelta(days=11, seconds=59628, microseconds=305862)),
            ("wIGCQ", timedelta(days=20, seconds=76575, microseconds=212452)),
            ("DPfkU", timedelta(days=13, seconds=19833, microseconds=407895)),
        ],
    }
    assert response.data.keys() == data.keys()
    for key, value in data.items():
        assert type(response.data[key]) is type(value), key


@pytest.mark.django_db
def test_course_analytics_no_permissions(teacher_api_client):
    response = teacher_api_client.get(
        reverse("coursera-api:course-detail", kwargs={"pk": "bmHtyVrIEee3CwoIJ_9DVg"})
    )
    # TODO: this should raise a 403
    assert response.status_code == 404, str(response.content)


@pytest.mark.django_db
def test_video_analytics_view(
    teacher_api_client, coursera_course_id, coursera_video_id
):
    response = teacher_api_client.get(
        reverse(
            "coursera-api:video-detail",
            kwargs={"course_id": coursera_course_id, "item_id": coursera_video_id},
        )
    )
    assert response.status_code == 200, str(response.content)


@pytest.mark.django_db
def test_video_analytics_no_permissions(teacher_api_client, coursera_video_id):
    response = teacher_api_client.get(
        reverse(
            "coursera-api:video-detail",
            kwargs={
                "course_id": "bmHtyVrIEee3CwoIJ_9DVg",
                "item_id": coursera_video_id,
            },
        )
    )
    # TODO: this should raise a 403
    assert (response.status_code == 404) or (
        (response.status_code == 200) and (response.data == "[]")
    ), str(response.content)
