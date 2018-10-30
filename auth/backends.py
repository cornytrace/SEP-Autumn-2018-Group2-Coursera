from datetime import datetime
from threading import local

from django.conf import settings
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

from auth.users import User


class OAuth2Backend:
    """
    Django Authentication backend that uses an external OAuth2 Authorization
    Server to validate the access token. 

    Does not depend on django.contrib.auth, and doesn't save a local copy of
    the user.
    """

    _local = local()
    access_token = {
        "access_token": settings.AUTHORIZATION_SERVER_ACCESS_TOKEN,
        "token_type": "Bearer",
        "scope": ["read", "write", "introspection"],
        "expires_at": 1_696_232_955.0,
    }

    def get_introspection_client(self):
        """
        Get an OAuth2 client configured with the resource server's access
        token. This client is reused for all requests in this thread.

        It's not apparent whetehr OAuth2Session is thread-safe and can thus be
        reused across every thread.
        """
        try:
            return self._local.client
        except AttributeError:
            self._local.client = OAuth2Session(token=self.access_token)
            return self._local.client

    def authenticate(self, request):
        """
        Retrieve the access token from the Authorization header, and validate
        it against the Authorization Server. If the token is active, return a
        User object with the retreived data.
        """
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
