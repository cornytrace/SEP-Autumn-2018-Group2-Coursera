class User:
    is_staff = False
    is_superuser = False

    def __init__(
        self,
        username=None,
        active=False,
        scope=None,
        role=None,
        courses=None,
        exp=None,
        client_id=None,
        **kwargs
    ):
        self.username = username
        self.is_authenticated = self.is_active = active
        self.is_anonymous = not active
        self.scopes = set(scope.split(" ") if scope else [])
        self.role = role
        self.courses = set(courses if courses else [])
        self.expires = exp
        self.client_id = client_id
        self.kwargs = kwargs
