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


class Estabelecimento(models.Model):
    cnes = models.CharField(max_length=30, primary_key=True)
    nome = models.CharField(max_length=60, blank=True)
    endereco = models.TextField()
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)

    class Meta:
        db_table = 'estabelecimento'

    def __str__(self):
        return f'({self.cnes}) {self.nome}'


class HorarioFuncionamento(models.Model):
    DIAS = [
        (1, _(u"Segunda")),
        (2, _(u"Terça")),
        (3, _(u"Quarta")),
        (4, _(u"Quinta")),
        (5, _(u"Sexta")),
        (6, _(u"Sábado")),
        (7, _(u"Domingo")),
    ]

    dia_semana = models.IntegerField(choices=DIAS)
    hora_abre = models.TimeField()
    hora_fecha = models.TimeField()
    data = models.DateTimeField(null=True)

    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)

    def __unicode__(self):
        return f'{self.dia_semana or self.data}'


class Usuario(AbstractUser):
    pass


class Perfil(models.Model):
    choices = (
        (0, u'Paciente'),
        (1, u'Profissional'),
        (2, u'Coordenador do SUS'),
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


class Vacina(models.Model):
    codigo = models.CharField(max_length=30, primary_key=True)
    nome = models.CharField(max_length=60, blank=True)
    tempo_aplicacao = models.IntegerField(verbose_name="Tempo de aplicação (minutos)", default=15)

    def __unicode__(self):
        return f'{self.nome} ({self.codigo})'


class HoraMarcada(models.Model):
    status_choices = (
        (0, u'Marcado'),
        (1, u'Concluído'),
        (2, u'Cancelado'),
    )
    data = models.DateTimeField()
    status = models.IntegerField(choices=status_choices)
    comentario = models.CharField(max_length=500)
    vacina = models.ForeignKey(Vacina, on_delete=models.CASCADE)
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Usuario, related_name='horas_paciente', on_delete=models.CASCADE)
    atendente = models.ForeignKey(Usuario, related_name='horas_atendente', on_delete=models.CASCADE)

    marcado_em = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return f'{self.data} {self.vacina}'


class VacinaEstocada(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    quantidade = models.IntegerField()
    quantidade_atual = models.IntegerField(null=True)
    vacina = models.ForeignKey(Vacina, on_delete=models.CASCADE)
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    hora_marcada = models.ForeignKey(HoraMarcada, null=True, on_delete=models.CASCADE)

    def __unicode__(self):
        return f'{self.quantidade} {self.vacina}'


class VacinaAplicada(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    vacina = models.ForeignKey(Vacina, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Usuario, related_name='vacinas_aplicadas', on_delete=models.CASCADE)
    hora_marcada = models.ForeignKey(HoraMarcada, null=True, on_delete=models.CASCADE)

    def __unicode__(self):
        return f'{self.vacina} em {self.paciente}'
