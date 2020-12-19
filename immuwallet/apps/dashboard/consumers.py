import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
# from medicao.redis_bloc import EnvRedis, RefreshBloc


class DashboardConsumer(WebsocketConsumer):
    # TODO: tornar essas funções assíncronas

    def connect(self):
        self.grupo = str(self.scope['user'].id)
        RefreshBloc.adicionar_cliente(self.scope['user'].id)
        async_to_sync(self.channel_layer.group_add)(
            self.grupo,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        RefreshBloc.remover_cliente(self.scope['user'].id)
        async_to_sync(self.channel_layer.group_discard)(
            self.grupo,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        RefreshBloc.refresh_ttl(self.scope['user'].id)

    def refresh(self, event):
        RefreshBloc.refresh_ttl(self.scope['user'].id)
        RefreshBloc.refresh_registros(self.scope['user'].id)
        self.send(text_data=json.dumps(event))
