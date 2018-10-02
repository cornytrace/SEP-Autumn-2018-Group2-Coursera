import pytest
from django.apps import apps
from django.db.models import ProtectedError


@pytest.mark.parametrize(
    "model",
    [model for model in apps.get_models() if model._meta.app_label == "coursera"],
)
def test_coursera_db_for_write(db_router, model):
    with pytest.raises(ProtectedError):
        db_router.db_for_write(model)
