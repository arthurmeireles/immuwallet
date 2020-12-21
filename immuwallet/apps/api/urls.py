from django.urls import path

import api.views as v

urlpatterns = [
    path('horas_marcadas/', v.HoraMarcadaApiView.as_view(), name='horas_marcadas'),
    path('horarios_funcionamento/', v.HorariosFuncionamentoApiView.as_view(), name='horarios_funcionamento'),
    path('vacinas/<int:pk>/', v.VacinasUsuarioApiView.as_view(), name='vacinas'),
]
