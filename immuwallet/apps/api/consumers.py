import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from api.fila_bloc import FilaBloc


class FilaConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            FilaBloc.GROUP,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            FilaBloc.GROUP,
            self.channel_name
        )

    def reload(self, event):
        self.send(text_data=json.dumps(event))
