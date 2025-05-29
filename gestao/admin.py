# gestao/admin.py
from django.contrib import admin
from .models import Fornecedor, Produto, AtividadeSistema

class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('nome_razao_social', 'cnpj', 'email', 'telefone', 'ativo', 'data_cadastro')
    search_fields = ('nome_razao_social', 'cnpj', 'email')
    list_filter = ('ativo', 'estado', 'cidade')
    readonly_fields = ('data_cadastro', 'data_atualizacao')

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'fornecedor', 'codigo_produto', 'preco_venda', 'unidade_medida', 'ativo', 'data_atualizacao')
    search_fields = ('nome', 'codigo_produto', 'fornecedor__nome_razao_social', 'fornecedor__nome_fantasia')
    list_filter = ('ativo', 'fornecedor', 'data_cadastro')
    autocomplete_fields = ['fornecedor']
    readonly_fields = ('data_cadastro', 'data_atualizacao')
    fieldsets = (
        (None, {
            'fields': ('nome', 'codigo_produto', 'descricao', 'ativo')
        }),
        ('Associação', {
            'fields': ('fornecedor',)
        }),
        ('Valores e Medidas', {
            'fields': ('preco_custo', 'preco_venda', 'unidade_medida')
        }),
        ('Datas de Controle', {
            'fields': ('data_cadastro', 'data_atualizacao'),
            'classes': ('collapse',),
        }),
    )

class AtividadeSistemaAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'usuario_display', 'get_acao_display', 'descricao_curta')
    list_filter = ('acao', 'timestamp', 'usuario')
    search_fields = ('usuario__username', 'descricao')
    readonly_fields = ('timestamp', 'usuario', 'acao', 'descricao', 'detalhes_adicionais')

    def usuario_display(self, obj):
        return obj.usuario.username if obj.usuario else "Sistema"
    usuario_display.short_description = "Usuário"

    def descricao_curta(self, obj):
        return (obj.descricao[:75] + '...') if len(obj.descricao) > 75 else obj.descricao
    descricao_curta.short_description = "Descrição"

admin.site.register(Fornecedor, FornecedorAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(AtividadeSistema, AtividadeSistemaAdmin)
