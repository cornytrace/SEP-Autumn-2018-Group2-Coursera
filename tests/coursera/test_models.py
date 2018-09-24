import pytest
from django.db.models import ProtectedError

from coursera.models import (
    Course,
    CourseBranch,
    CourseBranchModule,
    CourseGrade,
    CourseMembership,
    CoursePassingState,
    EITDigitalUser,
)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "model",
    [
        Course,
        CourseBranch,
        CourseBranchModule,
        CourseGrade,
        CourseMembership,
        CoursePassingState,
        EITDigitalUser,
    ],
)
def test_can_query_model(model):
    assert model.objects.first(), "Coursera database is empty"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "model",
    [
        Course,
        CourseBranch,
        CourseBranchModule,
        CourseGrade,
        CourseMembership,
        CoursePassingState,
        EITDigitalUser,
    ],
)
def test_cannot_save_model(model):
    with pytest.raises(ProtectedError):
        model.objects.create(pk="abc")
