from collections import Counter
from datetime import date, timedelta

import pytest
from django.urls import reverse

from coursera.models import Course
from coursera.serializers import CourseAnalyticsSerializer


@pytest.mark.django_db
@pytest.mark.freeze_time("2018-09-25 15:00")
def test_course_analytics_view(
    teacher_api_client, coursera_course_id, django_assert_max_num_queries
):
    with django_assert_max_num_queries(9) as captured:
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
            days=20, hours=20, minutes=5, seconds=9, microseconds=461_960
        ),
        "average_time_per_module": [
            ("sGiw3", timedelta(days=13, seconds=67594, microseconds=396_139)),
            ("mtiDN", timedelta(days=12, seconds=33541, microseconds=27827)),
            ("uNiMX", timedelta(days=18, seconds=44361, microseconds=173_885)),
            ("Cnbc7", timedelta(days=16, seconds=35902, microseconds=668_189)),
            ("Q5WbI", timedelta(days=18, seconds=23504, microseconds=143_258)),
            ("rXWW5", timedelta(days=16, seconds=62370, microseconds=129_438)),
            ("1TPfk", timedelta(days=10, seconds=69910, microseconds=959_793)),
            ("j2R4F", timedelta(days=11, seconds=59628, microseconds=305_862)),
            ("wIGCQ", timedelta(days=20, seconds=76575, microseconds=212_452)),
            ("DPfkU", timedelta(days=13, seconds=19833, microseconds=407_895)),
        ],
        "geo_data": [("US", 1337), ("NL", 80085)],
    }
    assert response.data.keys() == data.keys()
    for key, value in data.items():
        assert type(response.data[key]) is type(value), key


@pytest.mark.django_db
@pytest.mark.parametrize("filter_type", ["from_date", "to_date"])
def test_course_analytics_date_filter(
    teacher_api_client, coursera_course_id, filter_type
):
    filtered_response = teacher_api_client.get(
        reverse("coursera-api:course-detail", kwargs={"pk": coursera_course_id})
        + f"?{filter_type}=2018-09-20"
    )
    response = teacher_api_client.get(
        reverse("coursera-api:course-detail", kwargs={"pk": coursera_course_id})
    )
    assert filtered_response.status_code == 200, str(filtered_response.content)
    simple_keys = [
        "enrolled_learners",
        # "leaving_learners",
        "finished_learners",
        "modules",
        "quizzes",
        "assignments",
        "videos",
        "cohorts",
        # "average_time",
    ]
    list_keys = [
        "ratings",
        "finished_learners_over_time",
        # "leaving_learners_per_module",
        # "average_time_per_module",
    ]

    for key in simple_keys:
        assert filtered_response.data[key] <= response.data[key], key

    for key in list_keys:
        assert len(filtered_response.data[key]) <= len(response.data[key]), key
        for i, (filtered, unfiltered) in enumerate(
            zip(filtered_response.data[key], response.data[key])
        ):
            assert (
                filtered[1] <= unfiltered[1]
            ), f"filtered {key} at position {i} was more than unfiltered data"


@pytest.mark.django_db
def test_course_analytics_date_filter_in_future(teacher_api_client, coursera_course_id):
    filtered_response = teacher_api_client.get(
        reverse("coursera-api:course-detail", kwargs={"pk": coursera_course_id})
        + "?from_date="
        + (date.today() + timedelta(days=10 * 365)).strftime("%Y-%m-%d")
    )
    assert filtered_response.status_code == 200, str(filtered_response.content)
    simple_keys = [
        "enrolled_learners",
        # "leaving_learners",
        "finished_learners",
        "cohorts",
    ]
    list_keys = [
        "ratings",
        "finished_learners_over_time",
        # "leaving_learners_per_module",
        # "average_time_per_module",
    ]

    for key in simple_keys:
        assert filtered_response.data[key] == 0, key

    # assert filtered_response.data["average_time"] == timedelta(0)

    for key in list_keys:
        assert len(filtered_response.data[key]) == 0 or all(
            d[1] == 0 for d in filtered_response.data[key]
        )


@pytest.mark.django_db
def test_course_analytics_no_permissions(teacher_api_client):
    response = teacher_api_client.get(
        reverse("coursera-api:course-detail", kwargs={"pk": "bmHtyVrIEee3CwoIJ_9DVg"})
    )
    # TODO: this should raise a 403
    assert response.status_code == 404, str(response.content)


@pytest.mark.django_db
def test_course_list_view(teacher_api_client):
    response = teacher_api_client.get(reverse("coursera-api:course-list"))
    keys = ["id", "slug", "name", "level"]
    assert response.status_code == 200, str(response.content)
    assert len(response.data) > 0, "no courses returned"
    for item in response.data:
        assert list(item.keys()) == keys


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
    keys = [
        "id",
        "branch",
        "item_id",
        "lesson",
        "order",
        "type",
        "name",
        "optional",
        "watched_video",
        "finished_video",
        "video_comments",
        "video_likes",
        "video_dislikes",
        "next_item",
        "views_over_runtime",
    ]
    assert response.status_code == 200, str(response.content)
    assert list(response.data.keys()) == keys


@pytest.mark.django_db
@pytest.mark.parametrize("filter_type", ["from_date", "to_date"])
def test_video_analytics_date_filter(
    teacher_api_client, coursera_course_id, coursera_video_id, filter_type
):
    filtered_response = teacher_api_client.get(
        reverse(
            "coursera-api:video-detail",
            kwargs={"course_id": coursera_course_id, "item_id": coursera_video_id},
        )
        + f"?{filter_type}=2018-09-20"
    )
    response = teacher_api_client.get(
        reverse(
            "coursera-api:video-detail",
            kwargs={"course_id": coursera_course_id, "item_id": coursera_video_id},
        )
    )
    assert filtered_response.status_code == 200, str(filtered_response.content)
    simple_keys = [
        "watched_video",
        "finished_video",
        "video_comments",
        "video_likes",
        "video_dislikes",
    ]
    list_keys = ["views_over_runtime"]

    for key in simple_keys:
        assert filtered_response.data[key] <= response.data[key], key

    for key in list_keys:
        assert len(filtered_response.data[key]) == len(response.data[key]), key
        for i, (filtered, unfiltered) in enumerate(
            zip(filtered_response.data[key], response.data[key])
        ):
            assert (
                filtered[1] <= unfiltered[1]
            ), f"filtered {key} at position {i} was more than unfiltered data"


@pytest.mark.django_db
def test_video_analytics_date_filter_in_future(
    teacher_api_client, coursera_course_id, coursera_video_id
):
    filtered_response = teacher_api_client.get(
        reverse(
            "coursera-api:video-detail",
            kwargs={"course_id": coursera_course_id, "item_id": coursera_video_id},
        )
        + "?from_date="
        + (date.today() + timedelta(days=10 * 365)).strftime("%Y-%m-%d")
    )
    assert filtered_response.status_code == 200, str(filtered_response.content)
    simple_keys = [
        "watched_video",
        "finished_video",
        "video_comments",
        "video_likes",
        "video_dislikes",
    ]
    list_keys = ["views_over_runtime"]

    for key in simple_keys:
        assert filtered_response.data[key] == 0, key

    for key in list_keys:
        assert len(filtered_response.data[key]) == 0 or all(
            d[1] == 0 for d in filtered_response.data[key]
        )


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


@pytest.mark.django_db
def test_video_analytics_view_no_next_item(
    teacher_api_client, coursera_course_id, coursera_video_id
):
    response = teacher_api_client.get(
        reverse(
            "coursera-api:video-detail",
            kwargs={"course_id": coursera_course_id, "item_id": coursera_video_id},
        )
    )
    assert response.status_code == 200, str(response.content)
    assert (
        response.data["next_item"]["type"] == 0
    ), "item type is not 0 when there is no next item"
    assert (
        response.data["next_item"]["item_id"] == ""
    ), "item_id is not empty when there is no next item"


@pytest.mark.django_db
def test_video_analytics_view_next_item(
    teacher_api_client, coursera_course_id, coursera_video_id
):
    response = teacher_api_client.get(
        reverse(
            "coursera-api:video-detail",
            kwargs={"course_id": "oWawIRajEeWEjBINzvDOWw", "item_id": "Fzhxo"},
        )
    )
    assert response.status_code == 200, str(response.content)
    assert response.data["next_item"]["type"] == 1, "item type is not correct"
    assert response.data["next_item"]["item_id"] == "X9UsA", "item_id is not correct"


@pytest.mark.django_db
def test_video_analytics_view_next_item_quiz(
    teacher_api_client, coursera_course_id, coursera_video_id
):
    response = teacher_api_client.get(
        reverse(
            "coursera-api:video-detail",
            kwargs={"course_id": "oWawIRajEeWEjBINzvDOWw", "item_id": "JkPC4"},
        )
    )
    assert response.status_code == 200, str(response.content)
    assert response.data["next_item"]["type"] == 6, "item type is not correct"
    assert response.data["next_item"]["item_id"] == "bWwMd", "item_id is not correct"
    assert (
        response.data["next_item"]["category"] == "quiz"
    ), "item category is not correct"
    assert (
        response.data["next_item"]["passing_fraction"] == 0.680_134_680_134_680_1
    ), "item passing fraction is not correct"


@pytest.mark.django_db
def test_video_list_view(teacher_api_client, coursera_course_id):
    response = teacher_api_client.get(
        reverse("coursera-api:video-list", kwargs={"course_id": coursera_course_id})
    )
    keys = ["id", "branch", "item_id", "lesson", "order", "type", "name", "optional"]
    assert response.status_code == 200, str(response.content)
    assert len(response.data) > 0, "no videos returned"
    for item in response.data:
        assert list(item.keys()) == keys


@pytest.mark.django_db
def test_quiz_analytics_view(
    teacher_api_client,
    coursera_course_id,
    coursera_assessment_base_id,
    coursera_assessment_version,
):
    response = teacher_api_client.get(
        reverse(
            "coursera-api:quiz-detail",
            kwargs={
                "course_id": coursera_course_id,
                "base_id": coursera_assessment_base_id,
                "version": coursera_assessment_version,
            },
        )
    )
    keys = [
        "id",
        "base_id",
        "version",
        "name",
        "type",
        "update_timestamp",
        "passing_fraction",
        "graded",
        "average_grade",
        "grade_distribution",
        "average_attempts",
        "number_of_attempts",
        "correct_ratio_per_question",
        "quiz_comments",
        "quiz_likes",
        "quiz_dislikes",
        "last_attempt_average_grade",
        "last_attempt_grade_distribution",
    ]
    assert response.status_code == 200, str(response.content)
    assert list(response.data.keys()) == keys


@pytest.mark.django_db
@pytest.mark.parametrize("filter_type", ["from_date", "to_date"])
def test_quiz_analytics_date_filter(
    teacher_api_client,
    coursera_course_id,
    coursera_assessment_base_id,
    coursera_assessment_version,
    filter_type,
):
    filtered_response = teacher_api_client.get(
        reverse(
            "coursera-api:quiz-detail",
            kwargs={
                "course_id": coursera_course_id,
                "base_id": coursera_assessment_base_id,
                "version": coursera_assessment_version,
            },
        )
        + f"?{filter_type}=2018-09-20"
    )
    response = teacher_api_client.get(
        reverse(
            "coursera-api:quiz-detail",
            kwargs={
                "course_id": coursera_course_id,
                "base_id": coursera_assessment_base_id,
                "version": coursera_assessment_version,
            },
        )
    )
    assert filtered_response.status_code == 200, str(filtered_response.content)
    simple_keys = ["quiz_comments", "quiz_likes", "quiz_dislikes"]

    for key in simple_keys:
        assert filtered_response.data[key] <= response.data[key], key


@pytest.mark.django_db
def test_quiz_analytics_date_filter_in_future(
    teacher_api_client,
    coursera_course_id,
    coursera_assessment_base_id,
    coursera_assessment_version,
):
    filtered_response = teacher_api_client.get(
        reverse(
            "coursera-api:quiz-detail",
            kwargs={
                "course_id": coursera_course_id,
                "base_id": coursera_assessment_base_id,
                "version": coursera_assessment_version,
            },
        )
        + "?from_date="
        + (date.today() + timedelta(days=10 * 365)).strftime("%Y-%m-%d")
    )
    assert filtered_response.status_code == 200, str(filtered_response.content)
    simple_keys = [
        "average_grade",
        "average_attempts",
        "quiz_comments",
        "quiz_likes",
        "quiz_dislikes",
        "last_attempt_average_grade",
    ]
    list_keys = [
        "grade_distribution",
        "number_of_attempts",
        "correct_ratio_per_question",
        "last_attempt_grade_distribution",
    ]

    for key in simple_keys:
        assert filtered_response.data[key] == 0, key

    for key in list_keys:
        assert len(filtered_response.data[key]) == 0 or all(
            d[1] == 0 for d in filtered_response.data[key]
        )


@pytest.mark.django_db
def test_quiz_analytics_no_permissions(
    teacher_api_client, coursera_assessment_base_id, coursera_assessment_version
):
    response = teacher_api_client.get(
        reverse(
            "coursera-api:quiz-detail",
            kwargs={
                "course_id": "bmHtyVrIEee3CwoIJ_9DVg",
                "base_id": coursera_assessment_base_id,
                "version": coursera_assessment_version,
            },
        )
    )
    # TODO: this should raise a 403
    assert (response.status_code == 404) or (
        (response.status_code == 200) and (response.data == "[]")
    ), str(response.content)


@pytest.mark.django_db
def test_quiz_version_list_view(
    teacher_api_client, coursera_course_id, coursera_assessment_base_id
):
    response = teacher_api_client.get(
        reverse(
            "coursera-api:quiz-list",
            kwargs={
                "course_id": coursera_course_id,
                "base_id": coursera_assessment_base_id,
            },
        )
    )
    keys = [
        "id",
        "base_id",
        "version",
        "name",
        "type",
        "update_timestamp",
        "passing_fraction",
        "graded",
    ]
    assert response.status_code == 200, str(response.content)
    assert len(response.data) > 0, "no quizzes returned"
    for item in response.data:
        assert list(item.keys()) == keys


@pytest.mark.django_db
def test_quiz_list_view(teacher_api_client, coursera_course_id):
    response = teacher_api_client.get(
        reverse("coursera-api:quiz-list", kwargs={"course_id": coursera_course_id})
    )
    keys = [
        "id",
        "base_id",
        "version",
        "name",
        "type",
        "update_timestamp",
        "passing_fraction",
        "graded",
    ]
    assert response.status_code == 200, str(response.content)
    assert len(response.data) > 0, "no quizzes returned"
    for item in response.data:
        assert list(item.keys()) == keys
    base_id_counter = Counter([quiz["base_id"] for quiz in response.data])
    for base_id, count in base_id_counter.items():
        assert count == 1, f"Encountered {key} more than once"


@pytest.mark.django_db
def test_assignment_analytics_view(
    teacher_api_client, coursera_course_id, coursera_assignment_id
):
    response = teacher_api_client.get(
        reverse(
            "coursera-api:assignment-detail",
            kwargs={"course_id": coursera_course_id, "item_id": coursera_assignment_id},
        )
    )
    keys = ["id", "branch", "item_id", "lesson", "order", "type", "name", "optional", "submissions", "submission_ratio", "average_grade"]
    assert response.status_code == 200, str(response.content)
    assert list(response.data.keys()) == keys


@pytest.mark.django_db
@pytest.mark.parametrize("filter_type", ["from_date", "to_date"])
def test_assignment_analytics_date_filter(
    teacher_api_client, coursera_course_id, coursera_assignment_id, filter_type
):
    filtered_response = teacher_api_client.get(
        reverse(
            "coursera-api:assignment-detail",
            kwargs={"course_id": coursera_course_id, "item_id": coursera_assignment_id},
        )
        + f"?{filter_type}=2018-09-20"
    )
    response = teacher_api_client.get(
        reverse(
            "coursera-api:assignment-detail",
            kwargs={"course_id": coursera_course_id, "item_id": coursera_assignment_id},
        )
    )
    assert filtered_response.status_code == 200, str(filtered_response.content)
    
    assert filtered_response.data["submissions"] <= response.data["submissions"]


@pytest.mark.django_db
def test_assignment_analytics_date_filter_in_future(
    teacher_api_client, coursera_course_id, coursera_assignment_id
):
    filtered_response = teacher_api_client.get(
        reverse(
            "coursera-api:assignment-detail",
            kwargs={"course_id": coursera_course_id, "item_id": coursera_assignment_id},
        )
        + "?from_date="
        + (date.today() + timedelta(days=10 * 365)).strftime("%Y-%m-%d")
    )
    assert filtered_response.status_code == 200, str(filtered_response.content)
    simple_keys = [
        "submissions",
        "submission_ratio",
        "average_grade",
    ]

    for key in simple_keys:
        assert filtered_response.data[key] == 0, key


@pytest.mark.django_db
def test_assignment_analytics_no_permissions(teacher_api_client, coursera_assignment_id):
    response = teacher_api_client.get(
        reverse(
            "coursera-api:assignment-detail",
            kwargs={
                "course_id": "bmHtyVrIEee3CwoIJ_9DVg",
                "item_id": coursera_assignment_id,
            },
        )
    )
    # TODO: this should raise a 403
    assert (response.status_code == 404) or (
        (response.status_code == 200) and (response.data == "[]")
    ), str(response.content)

@pytest.mark.django_db
def test_assignment_list_view(teacher_api_client, coursera_course_id):
    response = teacher_api_client.get(
        reverse("coursera-api:assignment-list", kwargs={"course_id": coursera_course_id})
    )
    keys = ["id", "branch", "item_id", "lesson", "order", "type", "name", "optional"]
    assert response.status_code == 200, str(response.content)
    assert len(response.data) > 0, "no assignments returned"
    for item in response.data:
        assert list(item.keys()) == keys
