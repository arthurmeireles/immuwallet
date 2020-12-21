from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import HoraMarcadaSerializer, HorarioFuncionamentoSerializer, VacinaAplicadaSerializer
from dashboard.models import HoraMarcada, HorarioFuncionamento, Usuario, VacinaAplicada


class HoraMarcadaApiView(generics.ListAPIView):
    serializer_class = HoraMarcadaSerializer
    queryset = HoraMarcada.objects.filter(status__lte=HoraMarcada.ATENDIMENTO)

    def get(self, request, *args, **kwargs):
        estabelecimento = request.query_params.get('estabelecimento', None)

        horas = self.get_queryset()

        if estabelecimento:
            horas = horas.filter(estabelecimento=estabelecimento)

        serializer = HoraMarcadaSerializer(horas, many=True)

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    @staticmethod
    def post(request):
        id_hora_marcada = request.data.get('id', None)
        status_hora_marcada = request.data.get('status', None)

        hora_marcada = get_object_or_404(HoraMarcada, id=id_hora_marcada)
        hora_marcada.status = status_hora_marcada
        hora_marcada.save()

        return Response([], status=status.HTTP_202_ACCEPTED)


class HorariosFuncionamentoApiView(APIView):

    def get(self, request, *args, **kwargs):
        estabelecimento = request.query_params.get('estabelecimento', None)

        horarios = HorarioFuncionamento.objects.all()

        if estabelecimento:
            horarios = horarios.filter(estabelecimento=estabelecimento)

        serializer = HorarioFuncionamentoSerializer(horarios, many=True)

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, *args, **kwargs):
        pk = request.query_params.get('pk', None)
        if pk is None:
            raise APIException("Informe o parâmetro 'pk'!")
        get_object_or_404(HorarioFuncionamento, pk=pk).delete()
        return Response([], status=status.HTTP_202_ACCEPTED)


class VacinasUsuarioApiView(APIView):

    @staticmethod
    def get(request, *args, **kwargs):
        usuario_pk = kwargs.get('pk')
        usuario = get_object_or_404(Usuario, pk=usuario_pk)

        objetos = VacinaAplicada.objects.filter(paciente=usuario)

        serializer = VacinaAplicadaSerializer(objetos, many=True)

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
