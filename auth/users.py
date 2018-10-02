class User:
    is_anonymous = False
    is_authenticated = True
    is_staff = False
    is_superuser = False
    is_active = True

    def __init__(
        self,
        username=None,
        active=None,
        scope=None,
        role=None,
        courses=None,
        exp=None,
        client_id=None,
        **kwargs
    ):
        self.username = username
        self.active = active
        self.scopes = set(scope.split(" ") if scope else [])
        self.role = role
        self.courses = set(courses if courses else [])
        self.expires = exp
        self.client_id = client_id
        self.kwargs = kwargs
