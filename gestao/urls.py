# gestao/urls.py
from django.urls import path
from . import views

app_name = 'gestao'

urlpatterns = [
    path('fornecedores/', views.listar_fornecedores, name='listar_fornecedores'),
    path('fornecedores/novo/', views.criar_fornecedor, name='criar_fornecedor'),
    path('fornecedores/<int:id>/', views.detalhe_fornecedor, name='detalhe_fornecedor'),
    path('fornecedores/<int:id>/editar/', views.editar_fornecedor, name='editar_fornecedor'),
    path('fornecedores/<int:id>/excluir/', views.excluir_fornecedor, name='excluir_fornecedor'),
    path('fornecedores/<int:fornecedor_id>/produtos/', views.listar_produtos_por_fornecedor, name='listar_produtos_por_fornecedor'),
    path('produtos/', views.listar_produtos, name='listar_produtos'),
    path('produtos/novo/', views.criar_produto, name='criar_produto'),
    path('produtos/<int:id>/', views.detalhe_produto, name='detalhe_produto'),
    path('produtos/<int:id>/editar/', views.editar_produto, name='editar_produto'),
    path('produtos/<int:id>/excluir/', views.excluir_produto, name='excluir_produto'),
    path('relatorios/atividades/', views.relatorio_atividades, name='relatorio_atividades'),
]