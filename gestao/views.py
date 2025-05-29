# gestao/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages 
from .models import Fornecedor, AtividadeSistema
from .forms import FornecedorForm 
from django.contrib.auth.decorators import login_required 

def listar_fornecedores(request):
    fornecedores = Fornecedor.objects.all().order_by('nome_razao_social')
    context = {
        'fornecedores': fornecedores
    }
    
    return render(request, 'gestao/listar_fornecedores.html', context)

@login_required
def criar_fornecedor(request):
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            
            fornecedor = form.save()

            AtividadeSistema.objects.create(
                usuario=request.user,
                acao='CREATE',
                descricao=f"Fornecedor '{fornecedor.nome_razao_social}' (CNPJ: {fornecedor.cnpj}) foi criado."
            )

            messages.success(request, f"Fornecedor '{fornecedor.nome_razao_social}' cadastrado com sucesso!")
            return redirect('gestao:listar_fornecedores')
        else:
            messages.error(request, "Erro ao cadastrar fornecedor. Por favor, verifique os erros abaixo.")
    else:
        form = FornecedorForm()

    context = {
        'form': form,
        'titulo_pagina': 'Cadastrar Novo Fornecedor'
    }
    return render(request, 'gestao/form_fornecedor.html', context)

@login_required
def detalhe_fornecedor(request, id):
    fornecedor = get_object_or_404(Fornecedor, pk=id)

    AtividadeSistema.objects.create(
        usuario=request.user,
        acao='VIEW',
        descricao=f"Visualizou detalhes do fornecedor '{fornecedor.nome_razao_social}' (ID: {fornecedor.id})."
    )
    context = {
        'fornecedor': fornecedor,
        'titulo_pagina': f"Detalhes de {fornecedor.nome_razao_social}"
    }
    return render(request, 'gestao/detalhe_fornecedor.html', context)

@login_required
def editar_fornecedor(request, id):
    fornecedor = get_object_or_404(Fornecedor, pk=id)

    if request.method == 'POST':
    
        form = FornecedorForm(request.POST, instance=fornecedor)
        if form.is_valid():
            fornecedor_editado = form.save()

            if form.changed_data:
                campos_alterados_str = ", ".join(form.changed_data)
                descricao_log = f"Fornecedor '{fornecedor_editado.nome_razao_social}' (CNPJ: {fornecedor_editado.cnpj}) foi atualizado. Campos alterados: {campos_alterados_str}."
            else:
                descricao_log = f"Tentativa de atualização do fornecedor '{fornecedor_editado.nome_razao_social}' (CNPJ: {fornecedor_editado.cnpj}), mas nenhum dado foi alterado."

            AtividadeSistema.objects.create(
                usuario=request.user,
                acao='UPDATE',
                descricao=descricao_log
            )

            messages.success(request, f"Fornecedor '{fornecedor_editado.nome_razao_social}' atualizado com sucesso!")
            return redirect('gestao:detalhe_fornecedor', id=fornecedor_editado.id)
        else:
            messages.error(request, "Erro ao atualizar fornecedor. Por favor, verifique os erros abaixo.")
    else: 
        form = FornecedorForm(instance=fornecedor)

    context = {
        'form': form,
        'fornecedor': fornecedor,
        'titulo_pagina': f"Editar Fornecedor: {fornecedor.nome_razao_social}",
        'edit_mode': True
    }
    return render(request, 'gestao/form_fornecedor.html', context)

@login_required
def excluir_fornecedor(request, id):
    fornecedor = get_object_or_404(Fornecedor, pk=id)

    if request.method == 'POST':
        nome_fornecedor_excluido = fornecedor.nome_razao_social
        cnpj_fornecedor_excluido = fornecedor.cnpj

        fornecedor.delete()

        AtividadeSistema.objects.create(
            usuario=request.user,
            acao='DELETE',
            descricao=f"Fornecedor '{nome_fornecedor_excluido}' (CNPJ: {cnpj_fornecedor_excluido}) foi excluído."
        )
        messages.success(request, f"Fornecedor '{nome_fornecedor_excluido}' excluído com sucesso!")
        return redirect('gestao:listar_fornecedores')

    context = {
        'fornecedor': fornecedor,
        'titulo_pagina': f"Confirmar Exclusão de {fornecedor.nome_razao_social}"
    }
    return render(request, 'gestao/confirmar_exclusao_fornecedor.html', context)