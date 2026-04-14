from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from rest_framework_simplejwt.authentication import JWTAuthentication


@database_sync_to_async
def get_user_from_token(raw_token):
    authenticator = JWTAuthentication()
    validated_token = authenticator.get_validated_token(raw_token)
    return authenticator.get_user(validated_token)


class JwtQueryAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        close_old_connections()
        scope["user"] = AnonymousUser()
        query_string = scope.get("query_string", b"").decode()
        token = parse_qs(query_string).get("token", [None])[0]

        if token:
            try:
                scope["user"] = await get_user_from_token(token)
            except Exception:
                scope["user"] = AnonymousUser()

        return await self.inner(scope, receive, send)
