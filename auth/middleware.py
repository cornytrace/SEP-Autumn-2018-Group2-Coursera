from django.contrib.auth import authenticate
from django.utils.cache import patch_vary_headers
from django.utils.deprecation import MiddlewareMixin


class OAuth2TokenMiddleware(MiddlewareMixin):
    """
    Middleware for OAuth2 user authentication

    This middleware is able to work along with AuthenticationMiddleware and its behaviour depends
    on the order it's processed with.

    If it comes *after* AuthenticationMiddleware and request.user is valid, leave it as is and does
    not proceed with token validation. If request.user is the Anonymous user proceeds and try to
    authenticate the user using the OAuth2 access token.

    If it comes *before* AuthenticationMiddleware, or AuthenticationMiddleware is not used at all,
    tries to authenticate user with the OAuth2 access token and set request.user field. Setting
    also request._cached_user field makes AuthenticationMiddleware use that instead of the one from
    the session.

    It also adds "Authorization" to the "Vary" header, so that django's cache middleware or a
    reverse proxy can create proper cache keys.
    """

    def process_request(self, request):
        # do something only if request contains a Bearer token
        print(type(request))
        if request.META.get("HTTP_AUTHORIZATION", "").startswith("Bearer"):
            if not hasattr(request, "user") or request.user.is_anonymous:
                user = authenticate(request=request)
                if user:
                    request.user = request._user = request._cached_user = user
            else:  # pragma: no cover
                return None

    def process_response(self, request, response):
        patch_vary_headers(response, ("Authorization",))
        return response
