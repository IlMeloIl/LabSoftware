# gestao/forms.py
from django import forms
from .models import Fornecedor
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
                'placeholder': 'Ex: Empresa Exemplo LTDA',
                'class': 'form-input-text' 
            }),
            'cnpj': forms.TextInput(attrs={
                'placeholder': '00.000.000/0000-00',
                'class': 'form-input-text'
            }),
            'nome_fantasia': forms.TextInput(attrs={
                'placeholder': 'Ex: Nome Popular da Empresa (Opcional)',
                'class': 'form-input-text'
            }),
            'email': forms.EmailInput(attrs={ 
                'placeholder': 'contato@empresa.com (Opcional)',
                'class': 'form-input-email'
            }),
            'telefone': forms.TextInput(attrs={
                'placeholder': '(00) 00000-0000 ou (00) 0000-0000 (Opcional)',
                'class': 'form-input-text'
            }),
            'endereco': forms.TextInput(attrs={
                'placeholder': 'Ex: Rua Exemplo, 123, Bairro (Opcional)',
                'class': 'form-input-text'
            }),
            'cidade': forms.TextInput(attrs={
                'placeholder': 'Ex: São Paulo (Opcional)',
                'class': 'form-input-text'
            }),
            'estado': forms.TextInput(attrs={
                'placeholder': 'Ex: SP (Opcional, 2 letras)',
                'class': 'form-input-text',
                'maxlength': '2' 
            }),
            'cep': forms.TextInput(attrs={
                'placeholder': '00000-000 (Opcional)',
                'class': 'form-input-text'
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-input-checkbox'
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