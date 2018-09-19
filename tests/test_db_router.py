import pytest
from django.apps import apps
from django.db.models import ProtectedError

from eit_dashboard.db_router import COURSERA_APP, COURSERA_DB, DEFAULT_DB


@pytest.mark.parametrize(
    "model",
    [model for model in apps.get_models() if model._meta.app_label != COURSERA_APP],
)
def test_default_db_for_read(db_router, model):
    assert (
        db_router.db_for_read(model) is None
    ), f"wrong db for app {model._meta.app_label}"


@pytest.mark.parametrize(
    "model",
    [model for model in apps.get_models() if model._meta.app_label == COURSERA_APP],
)
def test_coursera_db_for_read(db_router, model):
    assert (
        db_router.db_for_read(model) == COURSERA_DB
    ), f"wrong db for app {COURSERA_APP}"


@pytest.mark.parametrize(
    "model",
    [model for model in apps.get_models() if model._meta.app_label != COURSERA_APP],
)
def test_default_db_for_write(db_router, model):
    assert (
        db_router.db_for_write(model) is None
    ), f"wrong db for app {model._meta.app_label}"


@pytest.mark.parametrize(
    "model",
    [model for model in apps.get_models() if model._meta.app_label == COURSERA_APP],
)
def test_coursera_db_for_write(db_router, model):
    with pytest.raises(ProtectedError):
        db_router.db_for_write(model)


@pytest.mark.parametrize(
    "app_label",
    [
        app_config.label
        for app_config in apps.get_app_configs()
        if app_config.label != COURSERA_APP
    ],
)
def test_allow_migrate_coursera(db_router, app_label):
    assert db_router.allow_migrate(
        DEFAULT_DB, app_label
    ), f"{app_label} can't migrate on default db"
    assert notdb_router.allow_migrate(
        COURSERA_DB, app_label
    ), f"{app_label} can migrate on coursera db"


def test_allow_migrate_coursera(db_router):
    assert not db_router.allow_migrate(
        DEFAULT_DB, COURSERA_APP
    ), "coursera can migrate on default db"
    assert db_router.allow_migrate(
        COURSERA_DB, COURSERA_APP
    ), "coursera can't migrate on coursera db"
