import pytest
from django.db.models import ProtectedError

from coursera.models import Course, CourseMembership, User


@pytest.mark.django_db
@pytest.mark.parametrize("model", [Course, CourseMembership, User])
def test_can_query_model(model):
    assert model.objects.all(), "Coursera database is empty"


@pytest.mark.django_db
@pytest.mark.parametrize("model", [Course, CourseMembership, User])
def test_cannot_save_model(model):
    with pytest.raises(ProtectedError):
        model.objects.create(pk="abc")
