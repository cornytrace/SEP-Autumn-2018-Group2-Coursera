import pytest
from django.db.models import ProtectedError

from coursera.models import (
    Branch,
    Course,
    CourseMembership,
    CourseProgress,
    CourseRating,
    EITDigitalUser,
    Grade,
    Item,
    ItemAssessment,
    ItemPeerAssignment,
    ItemProgrammingAssignment,
    ItemType,
    LastActivity,
    LastActivityPerModule,
    Lesson,
    Module,
    OnDemandSession,
    PassingState,
)

models = [
    Branch,
    Course,
    CourseMembership,
    CourseProgress,
    CourseRating,
    EITDigitalUser,
    Grade,
    Item,
    ItemAssessment,
    ItemPeerAssignment,
    ItemProgrammingAssignment,
    ItemType,
    LastActivity,
    LastActivityPerModule,
    Lesson,
    Module,
    OnDemandSession,
    PassingState,
]


@pytest.mark.django_db
@pytest.mark.parametrize("model", models)
def test_can_query_model(model):
    assert model.objects.all()[:1], "Coursera database is empty"


@pytest.mark.django_db
@pytest.mark.parametrize("model", models)
def test_cannot_save_model(model):
    with pytest.raises(ProtectedError):
        model.objects.create(pk="abc")


@pytest.mark.django_db
@pytest.mark.parametrize("model", models)
def test_can_access_foreign_keys(model):
    instance = model.objects.all()[0]
    for field in model._meta.fields:
        if field.many_to_one:
            assert getattr(
                instance, field.name
            ), f"Could not get foreign key {field.name} from model {model._meta.object_name}"
