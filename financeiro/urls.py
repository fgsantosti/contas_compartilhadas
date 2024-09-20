from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login_view', views.login_view, name='login_view'),
    path('autenticar_usuario', views.autenticar_usuario, name='autenticar_usuario'),
    path('home', views.home, name='home'),

    path('grupo/criar/', views.criar_grupo, name='criar_grupo'),
    path('grupo/<int:grupo_id>/', views.detalhes_grupo, name='detalhes_grupo'),
    path('grupo/<int:grupo_id>/adicionar_renda/', views.adicionar_renda, name='adicionar_renda'),
    path('grupo/<int:grupo_id>/adicionar_gasto/', views.adicionar_gasto, name='adicionar_gasto'),
    path('grupo/<int:grupo_id>/adicionar_membro/', views.adicionar_membro, name='adicionar_membro'),

    path('grupo/<int:grupo_id>/listar_gastos/', views.listar_gastos_por_data, name='listar_gastos'),
]
