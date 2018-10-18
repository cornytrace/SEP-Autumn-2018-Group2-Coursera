from datetime import datetime
from threading import local

from django.conf import settings
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

from auth.users import User


class OAuth2Backend:
    _local = local()
    access_token = {
        "access_token": settings.AUTHORIZATION_SERVER_ACCESS_TOKEN,
        "token_type": "Bearer",
        "scope": ["read", "write", "introspection"],
        "expires_at": 1_696_232_955.0,
    }

    def get_introspection_client(self):
        try:
            return self._local.client
        except AttributeError:
            self._local.client = OAuth2Session(token=self.access_token)
            return self._local.client

    def authenticate(self, request):
        client = self.get_introspection_client()
        if request.META.get("HTTP_AUTHORIZATION", "").startswith("Bearer"):
            token = request.META["HTTP_AUTHORIZATION"][len("Bearer") :].strip()
            response = client.post(
                f"{settings.AUTHORIZATION_SERVER_URL}/o/introspect/",
                data={"token": token, "platform": "coursera"},
            )
            if response.status_code == 200:
                data = response.json()
                if data["active"]:
                    return User(**data)
        return None
