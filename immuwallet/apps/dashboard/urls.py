from django.urls import path

import dashboard.views as v

urlpatterns = [
    path('', v.LPIndexView.as_view(), name='landingpage'),
    path('dashboard', v.IndexView.as_view(), name='index'),
    path('gereciar_usuarios/', v.ListaUsuariosView.as_view(), name='gerenciar_usuarios'),
    path('editar_usuario/<int:id>', v.editar_usuario_view, name='editar_usuario'),
    path('cadastrar_usuario/', v.cadastrar_usuario_view, name='cadastrar_usuario'),
    path('sucesso/', v.SucessoView.as_view(), name='sucesso'),
    path('login/', v.login_page, name='login'),
    path('logout/', v.logout_page, name='logout'),
]
