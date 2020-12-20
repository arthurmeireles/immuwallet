from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.serializers import HoraMarcadaSerializer
from dashboard.models import HoraMarcada


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
