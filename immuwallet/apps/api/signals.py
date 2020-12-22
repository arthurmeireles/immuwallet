from django.db.models.signals import post_save
from django.dispatch import receiver

from api.fila_bloc import FilaBloc
from api.utils import mandar_email
from dashboard.models import Usuario, HoraMarcada, VacinaAplicada


@receiver(post_save, sender=HoraMarcada)
def dispara_reload(sender, instance, **kwargs):
    FilaBloc.disparar_reload(instance.estabelecimento.pk)


@receiver(post_save, sender=HoraMarcada)
def hora_marcada_gera_vacina_aplicada(sender, instance, **kwargs):
    if instance.status == HoraMarcada.CONCLUIDO and not VacinaAplicada.objects.filter(hora_marcada=instance).exists():
        VacinaAplicada.objects.create(vacina=instance.vacina, paciente=instance.paciente, hora_marcada=instance)
    FilaBloc.disparar_reload(instance.estabelecimento.pk)


@receiver(post_save, sender=Usuario)
def dispara_email_novo_usuario(sender, instance, created, **kwargs):
    # mandar_email("Bem vindo ao Immuwallet", "Agora você é um usuário do immuwallet!", instance.email)
    if created:
        mandar_email("Bem vindo ao Immuwallet", "Agora você é um usuário do immuwallet!", instance.email)
