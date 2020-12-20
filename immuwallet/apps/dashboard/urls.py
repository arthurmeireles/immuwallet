from django.urls import path

import dashboard.views as v

urlpatterns = [
    path('', v.LPIndexView.as_view(), name='landingpage'),
    path('dashboard', v.IndexView.as_view(), name='index'),
    path('agendar', v.agendar_view, name='agendar'),
    path('gereciar_usuarios/', v.ListaUsuariosView.as_view(), name='gerenciar_usuarios'),
    path('editar_usuario/<int:id>', v.editar_usuario_view, name='editar_usuario'),
    path('cadastrar_usuario/', v.cadastrar_usuario_view, name='cadastrar_usuario'),
    path('cadastrar_vacina_estocada/', v.cadastrar_vacina_estocada_view, name='cadastrar_vacina_estocada'),
    path('cadastrar_horario/', v.cadastrar_horario_view, name='cadastrar_horario'),
    path('editar_horario/<int:id>', v.editar_horario_view, name='editar_horario'),
    path('gerenciar_horarios', v.GerenciarHorariosView.as_view(), name='gerenciar_horarios'),
    path('sucesso/', v.SucessoView.as_view(), name='sucesso'),
    path('login/', v.login_page, name='login'),
    path('logout/', v.logout_page, name='logout'),
]
