# Generated by Django 5.2.1 on 2025-05-29 13:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Fornecedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_razao_social', models.CharField(max_length=255, verbose_name='Nome/Razão Social')),
                ('cnpj', models.CharField(max_length=18, unique=True, verbose_name='CNPJ')),
                ('nome_fantasia', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nome Fantasia')),
                ('email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='E-mail')),
                ('telefone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Telefone')),
                ('endereco', models.CharField(blank=True, max_length=255, null=True, verbose_name='Endereço')),
                ('cidade', models.CharField(blank=True, max_length=100, null=True, verbose_name='Cidade')),
                ('estado', models.CharField(blank=True, max_length=2, null=True, verbose_name='UF')),
                ('cep', models.CharField(blank=True, max_length=9, null=True, verbose_name='CEP')),
                ('data_cadastro', models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')),
                ('data_atualizacao', models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
            ],
            options={
                'verbose_name': 'Fornecedor',
                'verbose_name_plural': 'Fornecedores',
                'ordering': ['nome_razao_social'],
            },
        ),
        migrations.CreateModel(
            name='AtividadeSistema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acao', models.CharField(choices=[('CREATE', 'Criação'), ('UPDATE', 'Atualização'), ('DELETE', 'Exclusão'), ('LOGIN', 'Login'), ('LOGOUT', 'Logout'), ('VIEW', 'Visualização'), ('ERROR', 'Erro no Sistema'), ('OTHER', 'Outra Ação')], max_length=10, verbose_name='Ação Realizada')),
                ('descricao', models.TextField(verbose_name='Descrição da Atividade')),
                ('detalhes_adicionais', models.JSONField(blank=True, null=True, verbose_name='Detalhes Adicionais (JSON)')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Timestamp')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Atividade do Sistema',
                'verbose_name_plural': 'Atividades do Sistema',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome do Produto')),
                ('descricao', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                ('codigo_produto', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='Código do Produto/SKU')),
                ('preco_custo', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Preço de Custo')),
                ('preco_venda', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Preço de Venda')),
                ('unidade_medida', models.CharField(blank=True, max_length=20, null=True, verbose_name='Unidade de Medida')),
                ('data_cadastro', models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')),
                ('data_atualizacao', models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('fornecedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produtos', to='gestao.fornecedor', verbose_name='Fornecedor')),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
                'ordering': ['nome'],
            },
        ),
    ]
