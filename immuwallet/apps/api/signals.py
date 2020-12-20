from django.db.models.signals import post_save
from django.dispatch import receiver

from api.fila_bloc import FilaBloc
from dashboard.models import HoraMarcada


@receiver(post_save, sender=HoraMarcada)
def dispara_reload(sender, instance, **kwargs):
    FilaBloc.disparar_reload(instance.estabelecimento.pk)
