from rest_framework import serializers

from dashboard.models import HoraMarcada, Usuario, Estabelecimento, Vacina, HorarioFuncionamento, VacinaAplicada


class EstabelecimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estabelecimento
        fields = ['nome']


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'get_full_name']


class VacinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacina
        fields = ['nome']


class HoraMarcadaSerializer(serializers.ModelSerializer):
    paciente = UsuarioSerializer()
    estabelecimento = EstabelecimentoSerializer()
    vacina = VacinaSerializer()

    class Meta:
        model = HoraMarcada
        fields = '__all__'


class HorarioFuncionamentoSerializer(serializers.ModelSerializer):
    estabelecimento = EstabelecimentoSerializer()
    nome = serializers.SerializerMethodField()

    @staticmethod
    def get_nome(obj):
        return str(obj)

    class Meta:
        model = HorarioFuncionamento
        fields = ['pk', 'estabelecimento', 'nome']


class VacinaAplicadaSerializer(serializers.ModelSerializer):
    hora_marcada = HoraMarcadaSerializer()
    vacina = VacinaSerializer()

    class Meta:
        model = VacinaAplicada
        fields = '__all__'
