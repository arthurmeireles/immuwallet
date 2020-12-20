from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Estado(models.Model):
    nome = models.CharField(max_length=30, db_column='nome')
    sigla = models.CharField(max_length=20, primary_key=True)
    regiao = models.CharField(max_length=30)

    class Meta:
        db_table = 'estado'

    def __unicode__(self):
        return '%s' % self.nome


class Municipio(models.Model):
    ibge = models.CharField(max_length=20, primary_key=True)
    nome = models.CharField(max_length=50, )
    estado = models.ForeignKey(
        Estado,
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'municipio'

    def __unicode__(self):
        return '%s' % self.nome


class Vacina(models.Model):
    codigo = models.CharField(max_length=30, primary_key=True)
    nome = models.CharField(max_length=60, blank=True)
    tempo_aplicacao = models.IntegerField(verbose_name="Tempo de aplicação (minutos)", default=15)

    def __str__(self):
        return f'{self.nome} ({self.codigo})'


class Estabelecimento(models.Model):
    cnes = models.CharField(max_length=30, primary_key=True)
    nome = models.CharField(max_length=60, blank=True)
    endereco = models.TextField()
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)

    class Meta:
        db_table = 'estabelecimento'

    def __str__(self):
        return f'({self.cnes}) {self.nome}'

    def horario_atendimento_disponivel(self, data: datetime, vacina: Vacina):
        achou_horario = False
        for horario in self.horariofuncionamento_set.filter(data__date=data.date()):
            data_final = (data + timedelta(minutes=vacina.tempo_aplicacao)).time()
            if horario.hora_abre <= data.time() and horario.hora_fecha >= data_final:
                achou_horario = True
                break

        if not achou_horario:
            for horario in self.horariofuncionamento_set.filter(dia_semana=data.weekday()):
                data_final = (data + timedelta(minutes=vacina.tempo_aplicacao)).time()
                if horario.hora_abre <= data.time() and horario.hora_fecha >= data_final:
                    achou_horario = True
                    break

        if not achou_horario:
            raise Exception('Fora do horário de atendimento.')

        return True


class HorarioFuncionamento(models.Model):
    DIAS = [
        (0, _(u"Segunda")),
        (1, _(u"Terça")),
        (2, _(u"Quarta")),
        (3, _(u"Quinta")),
        (4, _(u"Sexta")),
        (5, _(u"Sábado")),
        (6, _(u"Domingo")),
    ]

    dia_semana = models.IntegerField(choices=DIAS, null=True)
    hora_abre = models.TimeField()
    hora_fecha = models.TimeField()
    data = models.DateTimeField(null=True)

    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)

    def __str__(self):
        if self.data:
            return f"{self.data.date()} das {self.hora_abre} às {self.hora_fecha}"
        return f"{self.get_dia_semana_display()} das {self.hora_abre} às {self.hora_fecha}"


class Usuario(AbstractUser):

    @property
    def calcular_perfil(self):
        if Perfil.objects.filter(usuario=self).exists():
            return self.perfil.tipo
        return Perfil.PACIENTE

    @property
    def calcular_estabelecimento(self):
        if Perfil.objects.filter(usuario=self).exists():
            return None
        return self.perfil.estabelecimento.pk

    @property
    def eh_coordenador(self):
        return Perfil.objects.filter(usuario=self, tipo=Perfil.COORDENADOR).exists()

    @property
    def eh_paciente(self):
        return not Perfil.objects.filter(usuario=self, tipo__in=(Perfil.PROFISSIONAL, Perfil.COORDENADOR)).exists()


class Perfil(models.Model):
    PACIENTE = 0
    PROFISSIONAL = 1
    COORDENADOR = 2
    choices = (
        (PACIENTE, u'Paciente'),
        (PROFISSIONAL, u'Profissional'),
        (COORDENADOR, u'Coordenador do SUS'),
    )
    tipo = models.IntegerField(choices=choices)
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    class Meta:
        db_table = 'perfil'

    def __unicode__(self):
        return f'{self.usuario.get_full_name()} ({self.tipo})'


class HoraMarcada(models.Model):
    MARCADO = 0
    ATENDIMENTO = 1
    CANCELADO = 2
    CONCLUIDO = 3
    status_choices = (
        (MARCADO, u'Marcado'),
        (ATENDIMENTO, u'Em atendimento'),
        (CANCELADO, u'Cancelado'),
        (CONCLUIDO, u'Concluído'),
    )
    data = models.DateTimeField()
    status = models.IntegerField(choices=status_choices)
    comentario = models.CharField(max_length=500)
    vacina = models.ForeignKey(Vacina, on_delete=models.CASCADE)
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Usuario, related_name='horas_paciente', on_delete=models.CASCADE)
    atendente = models.ForeignKey(Usuario, related_name='horas_atendente', null=True, on_delete=models.CASCADE)

    marcado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['data']

    def __unicode__(self):
        return f'{self.data} {self.vacina}'


class VacinaEstocada(models.Model):
    data = models.DateTimeField()
    quantidade = models.IntegerField()
    quantidade_atual = models.IntegerField(null=True)
    vacina = models.ForeignKey(Vacina, on_delete=models.CASCADE)
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)

    cadastrado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantidade} {self.vacina}'


class VacinaAplicada(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    vacina = models.ForeignKey(Vacina, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Usuario, related_name='vacinas_aplicadas', on_delete=models.CASCADE)
    hora_marcada = models.ForeignKey(HoraMarcada, null=True, on_delete=models.CASCADE)

    def __unicode__(self):
        return f'{self.vacina} em {self.paciente}'
