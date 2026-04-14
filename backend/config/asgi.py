import os

import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
django.setup()

from apps.communications.auth import JwtQueryAuthMiddleware  # noqa: E402
from apps.communications.routing import websocket_urlpatterns  # noqa: E402

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JwtQueryAuthMiddleware(URLRouter(websocket_urlpatterns)),
})
