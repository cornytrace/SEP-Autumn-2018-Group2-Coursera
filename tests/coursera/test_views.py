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
    with django_assert_max_num_queries(10) as captured:
        response = teacher_api_client.get(
            reverse("coursera-api:course-detail", kwargs={"pk": coursera_course_id})
        )

    assert response.status_code == 200, str(response.content)
    keys = [
        "id",
        "slug",
        "name",
        "specialization",
        "level",
        "enrolled_learners",
        "leaving_learners",
        "ratings",
        "finished_learners",
        "paying_learners",
        "modules",
        "quizzes",
        "assignments",
        "videos",
        "cohorts",
        "finished_learners_over_time",
        "leaving_learners_per_module",
        "average_time",
        "average_time_per_module",
        "geo_data",
        "cohort_list",
    ]
    assert list(response.data.keys()) == keys


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
        "leaving_learners",
        "finished_learners",
        "paying_learners",
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
        "leaving_learners",
        "finished_learners",
        # "paying_learners",
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
@pytest.mark.parametrize("filter_type", ["from_date", "to_date"])
def test_course_analytics_invalid_date_filter(teacher_api_client, coursera_course_id, filter_type):
    response = teacher_api_client.get(
        reverse("coursera-api:course-detail", kwargs={"pk": coursera_course_id})
        + f"?{filter_type}=invalid"
    )
    assert response.status_code == 200, str(response.content)
    keys = [
        "id",
        "slug",
        "name",
        "specialization",
        "level",
        "enrolled_learners",
        "leaving_learners",
        "ratings",
        "finished_learners",
        "paying_learners",
        "modules",
        "quizzes",
        "assignments",
        "videos",
        "cohorts",
        "finished_learners_over_time",
        "leaving_learners_per_module",
        "average_time",
        "average_time_per_module",
        "geo_data",
        "cohort_list",
    ]
    assert list(response.data.keys()) == keys


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
    keys = [
        "id",
        "slug",
        "name",
        "specialization",
        "level",
        "enrolled_learners",
        "leaving_learners",
        "ratings",
        "finished_learners",
        "paying_learners",
    ]
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
        "next_video",
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
@pytest.mark.parametrize("filter_type", ["from_date", "to_date"])
def test_video_analytics_view_invalid_date_filter(
    teacher_api_client, coursera_course_id, coursera_video_id, filter_type
):
    response = teacher_api_client.get(
        reverse(
            "coursera-api:video-detail",
            kwargs={"course_id": coursera_course_id, "item_id": coursera_video_id},
        )
        + f"?{filter_type}=invalid"
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
        "next_video",
        "views_over_runtime",
    ]
    assert response.status_code == 200, str(response.content)
    assert list(response.data.keys()) == keys



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
    teacher_api_client, coursera_alt_course_id, coursera_video_id
):
    response = teacher_api_client.get(
        reverse(
            "coursera-api:video-detail",
            kwargs={"course_id": coursera_alt_course_id, "item_id": "Fzhxo"},
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
        "next_item",
        "next_quiz",
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
def test_quiz_analytics_next_quiz(teacher_api_client,
    coursera_alt_course_id,
):
    response = teacher_api_client.get(
        reverse(
            "coursera-api:quiz-detail",
            kwargs={
                "course_id": coursera_alt_course_id,
                "base_id": "9AgQAXM4EeWKJA7piulVWw",
                "version": 4,
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
        "next_item",
        "next_quiz",
    ]
    assert response.status_code == 200, str(response.content)
    assert list(response.data.keys()) == keys

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
    keys = ["id", "branch", "item_id", "lesson", "order", "type", "name", "optional", "submissions", "submission_ratio", "average_grade", "next_item", "next_assignment"]
    assert response.status_code == 200, str(response.content)
    assert list(response.data.keys()) == keys

@pytest.mark.django_db
def test_assignment_analytics_view_next_assignment(
    teacher_api_client, coursera_course_id, coursera_assignment_id
):
    response = teacher_api_client.get(
        reverse(
            "coursera-api:assignment-detail",
            kwargs={"course_id": "V4m7Xf5qEeS9ISIACxWDhA", "item_id": "PoQSi"},
        )
    )
    keys = ["id", "branch", "item_id", "lesson", "order", "type", "name", "optional", "submissions", "submission_ratio", "average_grade", "next_item", "next_assignment"]
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
    simple_keys = ["submissions", "submission_ratio", "average_grade"]

    for key in simple_keys:
        assert filtered_response.data[key] == 0, key


@pytest.mark.django_db
@pytest.mark.parametrize("filter_type", ["from_date", "to_date"])
def test_assignment_analytics_view_invalid_date_filter(
    teacher_api_client, coursera_course_id, coursera_assignment_id, filter_type
):
    response = teacher_api_client.get(
        reverse(
            "coursera-api:assignment-detail",
            kwargs={"course_id": coursera_course_id, "item_id": coursera_assignment_id},
        )
        + f"?{filter_type}=invalid"
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
        "submissions",
        "submission_ratio",
        "average_grade",
        "next_item",
        "next_assignment"
    ]
    assert response.status_code == 200, str(response.content)
    assert list(response.data.keys()) == keys



@pytest.mark.django_db
def test_assignment_analytics_no_permissions(
    teacher_api_client, coursera_assignment_id
):
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
        reverse(
            "coursera-api:assignment-list", kwargs={"course_id": coursera_course_id}
        )
    )
    keys = ["id", "branch", "item_id", "lesson", "order", "type", "name", "optional"]
    assert response.status_code == 200, str(response.content)
    assert len(response.data) > 0, "no assignments returned"
    for item in response.data:
        assert list(item.keys()) == keys
