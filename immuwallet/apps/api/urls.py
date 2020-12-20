from django.urls import path

import api.views as v

urlpatterns = [
    path('horas_marcadas/', v.HoraMarcadaApiView.as_view(), name='horas_marcadas'),
]
