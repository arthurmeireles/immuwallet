from rest_framework import serializers

from dashboard.models import HoraMarcada, Usuario, Estabelecimento, Vacina


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
