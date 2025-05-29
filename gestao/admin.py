# gestao/admin.py
from django.contrib import admin
from .models import Fornecedor, Produto, AtividadeSistema

class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('nome_razao_social', 'cnpj', 'email', 'telefone', 'ativo', 'data_cadastro')
    search_fields = ('nome_razao_social', 'cnpj', 'email')
    list_filter = ('ativo', 'estado', 'cidade')
    readonly_fields = ('data_cadastro', 'data_atualizacao')

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'fornecedor', 'codigo_produto', 'preco_venda', 'ativo')
    search_fields = ('nome', 'codigo_produto', 'fornecedor__nome_razao_social')
    list_filter = ('ativo', 'fornecedor')
    autocomplete_fields = ['fornecedor'] # Melhora a seleção de fornecedor se houver muitos

class AtividadeSistemaAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'usuario_display', 'get_acao_display', 'descricao_curta')
    list_filter = ('acao', 'timestamp', 'usuario')
    search_fields = ('usuario__username', 'descricao')
    readonly_fields = ('timestamp', 'usuario', 'acao', 'descricao', 'detalhes_adicionais') # Geralmente logs não são editáveis

    def usuario_display(self, obj):
        return obj.usuario.username if obj.usuario else "Sistema"
    usuario_display.short_description = "Usuário"

    def descricao_curta(self, obj):
        return (obj.descricao[:75] + '...') if len(obj.descricao) > 75 else obj.descricao
    descricao_curta.short_description = "Descrição"

admin.site.register(Fornecedor, FornecedorAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(AtividadeSistema, AtividadeSistemaAdmin)
