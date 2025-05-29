# gestao/admin.py
from django.contrib import admin
from .models import Fornecedor, Produto, AtividadeSistema

admin.site.register(Fornecedor)
admin.site.register(Produto)
admin.site.register(AtividadeSistema)
