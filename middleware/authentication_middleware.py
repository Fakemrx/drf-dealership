"""JWT Authentication Middleware"""
from django.utils.functional import SimpleLazyObject
from rest_framework_simplejwt.authentication import JWTAuthentication


def get_user(request):
    """Gets user by passing or not authentication."""
    try:
        user = JWTAuthentication().authenticate(request)[0]
        return user
    except TypeError:
        return None


class JwtUserMiddleware:
    """
    Middleware that looks at request, authorizes user through token
    and adds user to the response, it's made for balance
    change logics and offer create, otherwise it's just returning response.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/api/buyer/"):
            request.user = SimpleLazyObject(lambda: get_user(request))
            response = self.get_response(request)
            if hasattr(request, "user") and request.user is not None:
                response["X-User"] = request.user
            return response
        return self.get_response(request)
