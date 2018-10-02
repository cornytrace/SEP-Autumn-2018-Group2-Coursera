from django.db.models import ProtectedError


class DatabaseRouter:
    def db_for_write(self, model, **hints):
        raise ProtectedError(
            "No write access to 'coursera' database.", [hints.get("instance")]
        )
