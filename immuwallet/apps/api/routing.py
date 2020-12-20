from django.urls import re_path

from api.consumers import FilaConsumer

websocket_urlpatterns = [
    re_path(r'ws/fila/(?P<estabelecimento_id>\d+)/$', FilaConsumer.as_asgi()),
]
