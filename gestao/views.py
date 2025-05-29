# gestao/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages 
from .models import Fornecedor, Produto, AtividadeSistema
from .forms import FornecedorForm, ProdutoForm
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

@login_required
def listar_produtos_por_fornecedor(request, fornecedor_id):
    fornecedor = get_object_or_404(Fornecedor, pk=fornecedor_id)
    produtos = Produto.objects.filter(fornecedor=fornecedor).order_by('nome')

    AtividadeSistema.objects.create(
        usuario=request.user,
        acao='VIEW',
        descricao=f"Visualizou produtos do fornecedor '{fornecedor.nome_razao_social}' (ID: {fornecedor.id})."
    )

    context = {
        'produtos': produtos,
        'fornecedor': fornecedor,
        'titulo_pagina': f"Produtos de {fornecedor.nome_razao_social}"
    }

    return render(request, 'gestao/listar_produtos_do_fornecedor.html', context)

@login_required
def listar_produtos(request):
    produtos = Produto.objects.all().select_related('fornecedor').order_by('nome')
    context = {
        'produtos': produtos,
        'titulo_pagina': 'Lista de Produtos'
    }
    return render(request, 'gestao/listar_produtos.html', context)

@login_required
def detalhe_produto(request, id):
    produto = get_object_or_404(Produto.objects.select_related('fornecedor'), pk=id)
    AtividadeSistema.objects.create(
        usuario=request.user,
        acao='VIEW',
        descricao=f"Visualizou detalhes do produto '{produto.nome}' (ID: {produto.id})."
    )
    context = {
        'produto': produto,
        'titulo_pagina': f"Detalhes de {produto.nome}"
    }
    return render(request, 'gestao/detalhe_produto.html', context)

@login_required
def criar_produto(request):
    fornecedor_id_inicial = request.GET.get('fornecedor_id')
    fornecedor_selecionado_obj = None
    produto_pre_instance = None 

    if fornecedor_id_inicial:
        try:
            fornecedor_selecionado_obj = Fornecedor.objects.get(pk=fornecedor_id_inicial, ativo=True)
            produto_pre_instance = Produto(fornecedor=fornecedor_selecionado_obj)
        except Fornecedor.DoesNotExist:
            messages.warning(request, "Fornecedor inicial não encontrado ou inativo. Selecione um fornecedor manualmente.")
            fornecedor_selecionado_obj = None

    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto_pre_instance, fornecedor_fixo=fornecedor_selecionado_obj)
        if form.is_valid():
            produto = form.save(commit=False)
            # Se o fornecedor foi fixado e o campo estava desabilitado,
            # o valor pode não vir no form.cleaned_data.
            # A 'instance' passada ao formulário já deve ter o fornecedor correto.
            # Se, por algum motivo, a 'instance' não foi suficiente (ex: campo não era parte do modelo inicialmente),
            # você poderia reatribuir aqui:
            # if fornecedor_selecionado_obj and not produto.fornecedor:
            #    produto.fornecedor = fornecedor_selecionado_obj
            # Mas com a abordagem de passar 'instance=produto_pre_instance', isso deve ser automático.
            produto.save() 

            AtividadeSistema.objects.create(
                usuario=request.user,
                acao='CREATE',
                descricao=f"Produto '{produto.nome}' (Cód: {produto.codigo_produto or 'N/A'}) foi criado e associado ao fornecedor '{produto.fornecedor.nome_razao_social}'."
            )
            messages.success(request, f"Produto '{produto.nome}' cadastrado com sucesso!")

            if fornecedor_selecionado_obj:
                 return redirect('gestao:listar_produtos_por_fornecedor', fornecedor_id=produto.fornecedor.id)
            return redirect('gestao:listar_produtos')
        else:
            messages.error(request, "Erro ao cadastrar produto. Por favor, verifique os erros abaixo.")
    else:
        form = ProdutoForm(instance=produto_pre_instance, fornecedor_fixo=fornecedor_selecionado_obj)

    context = {
        'form': form,
        'titulo_pagina': 'Cadastrar Novo Produto',
        'edit_mode': False,
        'fornecedor_selecionado': fornecedor_selecionado_obj
    }
    return render(request, 'gestao/form_produto.html', context)

@login_required
def editar_produto(request, id):
    produto = get_object_or_404(Produto, pk=id) 

    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            produto_editado = form.save()

            if form.changed_data:
                campos_alterados_str = ", ".join(form.changed_data)
                descricao_log = f"Produto '{produto_editado.nome}' (Cód: {produto_editado.codigo_produto or 'N/A'}) foi atualizado. Campos alterados: {campos_alterados_str}."
            else:
                descricao_log = f"Tentativa de atualização do produto '{produto_editado.nome}' (Cód: {produto_editado.codigo_produto or 'N/A'}), mas nenhum dado foi alterado."

            AtividadeSistema.objects.create(
                usuario=request.user,
                acao='UPDATE',
                descricao=descricao_log
            )
            messages.success(request, f"Produto '{produto_editado.nome}' atualizado com sucesso!")
            return redirect('gestao:detalhe_produto', id=produto_editado.id)
        else:
            messages.error(request, "Erro ao atualizar produto. Por favor, verifique os erros abaixo.")
    else:
        form = ProdutoForm(instance=produto)

    context = {
        'form': form,
        'produto': produto,
        'titulo_pagina': f"Editar Produto: {produto.nome}",
        'edit_mode': True
    }
    return render(request, 'gestao/form_produto.html', context)

@login_required
def excluir_produto(request, id):
    produto = get_object_or_404(Produto, pk=id)
    if request.method == 'POST':
        nome_produto_excluido = produto.nome
        codigo_produto_excluido = produto.codigo_produto or 'N/A'

        produto.delete()

        AtividadeSistema.objects.create(
            usuario=request.user,
            acao='DELETE',
            descricao=f"Produto '{nome_produto_excluido}' (Cód: {codigo_produto_excluido}) foi excluído."
        )
        messages.success(request, f"Produto '{nome_produto_excluido}' excluído com sucesso!")
        return redirect('gestao:listar_produtos')

    context = {
        'produto': produto,
        'titulo_pagina': f"Confirmar Exclusão de {produto.nome}"
    }
    return render(request, 'gestao/confirmar_exclusao_produto.html', context)