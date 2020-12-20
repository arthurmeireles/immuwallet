from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from redis import Redis

redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)


class FilaBloc:
    GROUP = 'fila_bloc'

    @staticmethod
    def disparar_reload(estabelecimento_id):
        """
        Avisa no grupo que houve mudança na fila do estabelecimento
        """
        layer = get_channel_layer()
        async_to_sync(layer.group_send)(
            FilaBloc.GROUP,
            {
                'type': 'reload',
                'value': estabelecimento_id
            }
        )
