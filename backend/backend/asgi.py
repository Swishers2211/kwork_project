import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from chat.middleware import JWTAuthMiddleware

django.setup()

from chat.routing import websocket_urlpatterns

import chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
	{
		'http': django_asgi_app,
		'websocket': AllowedHostsOriginValidator(JWTAuthMiddleware(URLRouter(websocket_urlpatterns))),
	}
)
