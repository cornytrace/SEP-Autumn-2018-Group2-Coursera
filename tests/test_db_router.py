import pytest
from django.apps import apps
from django.db.models import ProtectedError


@pytest.mark.parametrize(
    "model",
    [model for model in apps.get_models() if model._meta.app_label == "coursera"],
)
def test_coursera_db_for_write(db_router, model):
    """
    Test that trying to write to the coursera database raises a ProtectedError.
    """
    with pytest.raises(ProtectedError):
        db_router.db_for_write(model)
