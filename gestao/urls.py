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
]