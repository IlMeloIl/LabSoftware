# gestao/models.py
from django.db import models
from django.contrib.auth.models import User 

class Fornecedor(models.Model):
    nome_razao_social = models.CharField(max_length=255, verbose_name="Nome/Razão Social")
    cnpj = models.CharField(max_length=18, unique=True, verbose_name="CNPJ")
    nome_fantasia = models.CharField(max_length=255, blank=True, null=True, verbose_name="Nome Fantasia")
    email = models.EmailField(max_length=255, blank=True, null=True, verbose_name="E-mail")
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    endereco = models.CharField(max_length=255, blank=True, null=True, verbose_name="Endereço")
    cidade = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cidade")
    estado = models.CharField(max_length=2, blank=True, null=True, verbose_name="UF")
    cep = models.CharField(max_length=9, blank=True, null=True, verbose_name="CEP")
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")

    @property
    def cnpj_formatado(self):
        if self.cnpj and len(self.cnpj) == 14:
            return f"{self.cnpj[:2]}.{self.cnpj[2:5]}.{self.cnpj[5:8]}/{self.cnpj[8:12]}-{self.cnpj[12:]}"
        return self.cnpj

    @property
    def telefone_formatado(self):
        if self.telefone:
            if len(self.telefone) == 11: # Celular com 9º dígito
                return f"({self.telefone[:2]}) {self.telefone[2:7]}-{self.telefone[7:]}"
            elif len(self.telefone) == 10: # Fixo ou celular sem 9º
                return f"({self.telefone[:2]}) {self.telefone[2:6]}-{self.telefone[6:]}"
        return self.telefone

    @property
    def cep_formatado(self):
        if self.cep and len(self.cep) == 8:
            return f"{self.cep[:5]}-{self.cep[5:]}"
        return self.cep

    def __str__(self):
        return self.nome_razao_social

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        ordering = ['nome_razao_social']

class Produto(models.Model):
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, related_name="produtos", verbose_name="Fornecedor")
    nome = models.CharField(max_length=255, verbose_name="Nome do Produto")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    codigo_produto = models.CharField(max_length=50, blank=True, null=True, unique=True, verbose_name="Código do Produto/SKU")
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Preço de Custo")
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Preço de Venda")
    unidade_medida = models.CharField(max_length=20, blank=True, null=True, verbose_name="Unidade de Medida")
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")

    def __str__(self):
        return f"{self.nome} ({self.fornecedor.nome_razao_social})"

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['nome']

class AtividadeSistema(models.Model):
    TIPO_ACAO_CHOICES = [
        ('CREATE', 'Criação'),
        ('UPDATE', 'Atualização'),
        ('DELETE', 'Exclusão'),
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('VIEW', 'Visualização'),
        ('ERROR', 'Erro no Sistema'),
        ('OTHER', 'Outra Ação'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Usuário")
    acao = models.CharField(max_length=10, choices=TIPO_ACAO_CHOICES, verbose_name="Ação Realizada")
    descricao = models.TextField(verbose_name="Descrição da Atividade")
    detalhes_adicionais = models.JSONField(blank=True, null=True, verbose_name="Detalhes Adicionais (JSON)")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp")

    def __str__(self):
        user_display = self.usuario.username if self.usuario else "Sistema"
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {user_display} - {self.get_acao_display()}"

    class Meta:
        verbose_name = "Atividade do Sistema"
        verbose_name_plural = "Atividades do Sistema"
        ordering = ['-timestamp']