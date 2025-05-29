# gestao/forms.py
from django import forms
from .models import Fornecedor, Produto
import re 

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = [
            'nome_razao_social',
            'cnpj',
            'nome_fantasia',
            'email',
            'telefone',
            'endereco',
            'cidade',
            'estado',
            'cep',
            'ativo',
        ]

        
        widgets = {
            'nome_razao_social': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Empresa Exemplo LTDA'
            }),
            'cnpj': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '00.000.000/0000-00'
            }),
            'nome_fantasia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Nome Popular da Empresa (Opcional)'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'contato@empresa.com (Opcional)'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 0000-0000 ou (00) 00000-0000 (Opcional)'
            }),
            'endereco': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Rua Exemplo, 123, Bairro (Opcional)'
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: São Paulo (Opcional)'
            }),
            'estado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: SP (Opcional, 2 letras)',
                'maxlength': '2'
            }),
            'cep': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '00000-000 (Opcional)'
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

        
        labels = {
            'nome_razao_social': 'Nome/Razão Social Completa',
            'cnpj': 'CNPJ (Cadastro Nacional da Pessoa Jurídica)',
            'nome_fantasia': 'Nome Fantasia',
            'email': 'Endereço de E-mail Principal',
            'telefone': 'Telefone de Contato',
            'endereco': 'Endereço Completo',
            'cidade': 'Cidade',
            'estado': 'UF (Estado)',
            'cep': 'CEP (Código de Endereçamento Postal)',
            'ativo': 'Fornecedor Ativo?',
        }

        
        help_texts = {
            'cnpj': 'Informe apenas os números ou o CNPJ formatado. A formatação será ajustada.',
            'estado': 'Informe a sigla do estado com 2 letras (ex: SP, RJ, MG).',
            'telefone': 'Inclua o DDD.',
        }

    def clean_nome_razao_social(self):
        nome = self.cleaned_data.get('nome_razao_social')
        if nome and len(nome.strip()) < 3: 
            raise forms.ValidationError("O nome/razão social deve ter pelo menos 3 caracteres significativos.")
        
        return nome.strip() if nome else nome

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        if not cnpj: 
            raise forms.ValidationError("O CNPJ é obrigatório.")

        cnpj_limpo = re.sub(r'[^0-9]', '', str(cnpj)) 

        if not cnpj_limpo and self.fields['cnpj'].required:
             raise forms.ValidationError("O CNPJ é obrigatório e deve conter números.")

        if cnpj_limpo: 
            if len(cnpj_limpo) != 14:
                raise forms.ValidationError("O CNPJ deve conter 14 dígitos numéricos.")
            return cnpj_limpo

        return cnpj 


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            return email.lower().strip()
        return email 

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            telefone_limpo = re.sub(r'[^0-9]', '', telefone)
            if not telefone_limpo: 
                 if self.fields['telefone'].required: 
                    raise forms.ValidationError("O telefone deve conter números.")
                 else:
                    return None 

            if not (10 <= len(telefone_limpo) <= 11):
                raise forms.ValidationError("O telefone deve conter entre 10 e 11 dígitos numéricos (incluindo DDD).")
            return telefone_limpo
        return telefone 

    def clean_cep(self):
        cep = self.cleaned_data.get('cep')
        if cep:
            cep_limpo = re.sub(r'[^0-9]', '', cep)
            if not cep_limpo:
                if self.fields['cep'].required:
                    raise forms.ValidationError("O CEP deve conter números.")
                else:
                    return None

            if len(cep_limpo) != 8:
                raise forms.ValidationError("O CEP deve conter 8 dígitos numéricos.")
            return cep_limpo
        return cep 

    def clean_estado(self):
        estado = self.cleaned_data.get('estado')
        if estado:
            estado_limpo = estado.strip().upper()
            if not re.match(r'^[A-Z]{2}$', estado_limpo):
                raise forms.ValidationError("A UF (Estado) deve conter exatamente 2 letras.")            
            return estado_limpo
        return estado 

    def clean_nome_fantasia(self):
        nome = self.cleaned_data.get('nome_fantasia')
        return nome.strip() if nome else nome

    def clean_endereco(self):
        endereco = self.cleaned_data.get('endereco')
        return endereco.strip() if endereco else endereco

    def clean_cidade(self):
        cidade = self.cleaned_data.get('cidade')
        return cidade.strip() if cidade else cidade

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            'nome',
            'descricao',
            'codigo_produto',
            'fornecedor',
            'preco_custo',
            'preco_venda',
            'unidade_medida',
            'ativo',
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Parafuso Sextavado 1/4"'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Detalhes adicionais sobre o produto (opcional)'}),
            'codigo_produto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: SKU12345 (Opcional, deve ser único)'}),
            'fornecedor': forms.Select(attrs={'class': 'form-select'}),
            'preco_custo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}),
            'preco_venda': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}),
            'unidade_medida': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: UN, KG, PC, CX (Opcional)'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nome': 'Nome do Produto',
            'descricao': 'Descrição Detalhada',
            'codigo_produto': 'Código do Produto/SKU',
            'fornecedor': 'Fornecedor Associado',
            'preco_custo': 'Preço de Custo (R$)',
            'preco_venda': 'Preço de Venda (R$)',
            'unidade_medida': 'Unidade de Medida',
            'ativo': 'Produto Ativo?',
        }
        help_texts = {
            'codigo_produto': 'Se informado, deve ser um código único para o produto.',
            'preco_custo': 'Utilize ponto como separador decimal (ex: 10.50).',
            'preco_venda': 'Utilize ponto como separador decimal (ex: 15.75).',
        }

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if nome and len(nome.strip()) < 2:
            raise forms.ValidationError("O nome do produto deve ter pelo menos 2 caracteres.")
        return nome.strip() if nome else nome

    def clean_codigo_produto(self):
        codigo = self.cleaned_data.get('codigo_produto')
        if codigo:
            instance = getattr(self, 'instance', None)
            query = Produto.objects.filter(codigo_produto__iexact=codigo.strip())
            if instance and instance.pk:
                query = query.exclude(pk=instance.pk)
            if query.exists():
                raise forms.ValidationError("Já existe um produto cadastrado com este código.")
            return codigo.strip()
        return codigo

    def clean_preco_custo(self):
        preco = self.cleaned_data.get('preco_custo')
        if preco is not None and preco < 0:
            raise forms.ValidationError("O preço de custo não pode ser negativo.")
        return preco

    def clean_preco_venda(self):
        preco = self.cleaned_data.get('preco_venda')
        if preco is not None and preco < 0:
            raise forms.ValidationError("O preço de venda não pode ser negativo.")
        return preco

    def __init__(self, *args, **kwargs):
        
        fornecedor_obj_fixo = kwargs.pop('fornecedor_fixo', None)
        
        editando_produto_existente = kwargs.get('instance') and kwargs.get('instance').pk

        super().__init__(*args, **kwargs)

        self.fields['fornecedor'].queryset = Fornecedor.objects.filter(ativo=True).order_by('nome_razao_social')

        if fornecedor_obj_fixo:
            self.fields['fornecedor'].initial = fornecedor_obj_fixo
            self.fields['fornecedor'].disabled = True
            
        elif editando_produto_existente:
            self.fields['fornecedor'].disabled = True