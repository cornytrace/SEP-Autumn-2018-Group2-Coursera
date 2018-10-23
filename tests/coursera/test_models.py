import pytest
from django.db.models import ProtectedError
from django.db.models.base import ModelBase

from coursera import models

model_list = [
    model
    for model in models.__dict__.values()
    if isinstance(model, ModelBase) and model is not models.ItemProgrammingAssignment
]


@pytest.mark.django_db
@pytest.mark.parametrize("model", model_list)
def test_can_query_model(model):
    assert model.objects.all()[:1], "Coursera database is empty"


@pytest.mark.django_db
@pytest.mark.parametrize("model", model_list)
def test_cannot_save_model(model):
    with pytest.raises(ProtectedError):
        model.objects.create(pk="abc")


@pytest.mark.django_db
@pytest.mark.parametrize("model", model_list)
def test_can_access_foreign_keys(model):
    instance = model.objects.all()[0]
    for field in model._meta.fields:
        if field.many_to_one:
            assert hasattr(
                instance, field.name
            ), f"Could not get foreign key {field.name} from model {model._meta.object_name}"
