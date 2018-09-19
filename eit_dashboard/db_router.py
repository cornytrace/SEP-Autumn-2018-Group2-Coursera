from django.db.models import ProtectedError

DEFAULT_DB = "default"
COURSERA_DB = "coursera"
COURSERA_APP = "coursera"


class DatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == COURSERA_APP:
            return COURSERA_DB
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == COURSERA_APP:
            raise ProtectedError(
                "No write access to 'coursera' database.", [hints.get("instance")]
            )
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == COURSERA_APP:
            return db == COURSERA_DB
        return db == DEFAULT_DB
