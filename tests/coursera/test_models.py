import pytest
from django.db.models import ProtectedError

from coursera.models import (
    Branch,
    Course,
    CourseMembership,
    CourseProgress,
    EITDigitalUser,
    Grade,
    Item,
    Lesson,
    Module,
    OnDemandSession,
    PassingState,
)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "model",
    [
        Branch,
        Course,
        CourseMembership,
        CourseProgress,
        EITDigitalUser,
        Grade,
        Item,
        Lesson,
        Module,
        OnDemandSession,
        PassingState,
    ],
)
def test_can_query_model(model):
    assert model.objects.all()[:1], "Coursera database is empty"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "model",
    [
        Branch,
        Course,
        CourseMembership,
        CourseProgress,
        EITDigitalUser,
        Grade,
        Item,
        Lesson,
        Module,
        OnDemandSession,
        PassingState,
    ],
)
def test_cannot_save_model(model):
    with pytest.raises(ProtectedError):
        model.objects.create(pk="abc")
