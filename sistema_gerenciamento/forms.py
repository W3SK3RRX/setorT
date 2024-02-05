# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import validators
from .models import Veiculo, Manutencao, Checklist, User, Motorista, Combustivel, Rota, Demanda, Viagem
import re
from django.utils import timezone


class CadastroForm(UserCreationForm):
    error_messages = {
        'password_mismatch': 'As senhas não coincidem.',
        'invalid_username': 'O nome de usuário deve conter apenas letras, números e sublinhados.',
        'email_in_use': 'Este endereço de email já está em uso.',
        'invalid_password': 'A senha deve conter pelo menos um número e uma letra.',
    }

    username = forms.CharField(
        label='Usuário:',
        max_length=30,
        validators=[
            validators.RegexValidator(
                regex='^[a-zA-Z0-9_]+$',
                message= 'O nome de usuário deve conter apenas letras, números e sublinhados.',
                code='invalid_username'
            ),
        ],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    email = forms.EmailField(
        label='Email:',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(self.error_messages['email_in_use'])
        return email

    password1 = forms.CharField(
        label='Senha:',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators=[
            validators.MinLengthValidator(
                limit_value=8,
                message='A senha deve ter pelo menos 8 caracteres.',
            ),
            validators.RegexValidator(
                regex='^(?=.*[0-9])(?=.*[a-zA-Z]).*$',
                message='A senha deve conter pelo menos um número e uma letra.',
                code='invalid_password',
            ),
        ],
    )

    password2 = forms.CharField(
        label='Confirme a senha:',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'username': 'Usuário:',
            'email': 'Email:',
            'password1': 'Senha:',
        }

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        return password1


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Nome de Usuário:',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={
            'invalid_login': 'Nome de usuário ou senha incorretos.',
            'inactive': 'Esta conta está inativa.',
        },
    )
    password = forms.CharField(
        label='Senha:',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        error_messages={
            'invalid_login': 'Nome de usuário ou senha incorretos.',
            'inactive': 'Esta conta está inativa.',
        },
    )


class VeiculoForm(forms.ModelForm):
    ESTADO_FUNCIONAMENTO_CHOICES = [
        ('Funcional', 'Funcional'),
        ('Não Funcional', 'Não Funcional'),
    ]

    estado_funcionamento = forms.ChoiceField(
        choices=ESTADO_FUNCIONAMENTO_CHOICES,
        required=True,
        label='Estado de funcionamento:',
        widget=forms.RadioSelect(attrs={'class': 'list-unstyled'})
    )

    class Meta:
        model = Veiculo
        fields = ['modelo', 'fabricante', 'ano', 'placa', 'data_cadastro', 'estado_funcionamento']
        widgets = {
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'fabricante': forms.TextInput(attrs={'class': 'form-control'}),
            'ano': forms.NumberInput(attrs={'class': 'form-control'}),
            'placa': forms.TextInput(attrs={'class': 'form-control'}),
            'data_cadastro': forms.DateInput(attrs={'type':'date', 'class': 'form-control', 'placeholder': 'dd/mm/aaaa'}),
        }

        labels = {
            'modelo': 'Modelo:',
            'fabricante': 'Fabricante:',
            'ano': 'Ano:',
            'placa': 'Placa:',
            'data_cadastro': 'Data:',
        }


class ManutencaoForm(forms.ModelForm):
    class Meta:
        model = Manutencao
        fields = ['veiculo', 'data', 'descricao_manutencao', 'comprovante_manutencao']

        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'dd/mm/aaaa'}),
            'descricao_manutencao': forms.Textarea(attrs={'class': 'form-control'}),
            'comprovante_manutencao': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

        labels = {
            'data': 'Data:',
            'descricao_manutencao': 'Descrição:',
            'comprovante_manutencao': 'Comprovante:',
        }

    def __init__(self, *args, **kwargs):
        super(ManutencaoForm, self).__init__(*args, **kwargs)
        # Adiciona um campo de seleção para os modelos de veículos
        self.fields['veiculo'] = forms.ModelChoiceField(
            label='Veículo:',
            queryset=Veiculo.objects.all(),
            empty_label="Selecione o veículo"
        )
        self.fields['veiculo'].widget.attrs.update({'class': ' form-control col-sm-8 mx-auto'})


class ChecklistForm(forms.ModelForm):
    class Meta:
        model = Checklist
        fields = ['veiculo', 'data', 'comprovante_checklist']

        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'dd/mm/aaaa'}),
            'comprovante_checklist': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

        labels = {
            'data':'Data:',
            'comprovante_checklist':'Comprovante:',
        }

    def __init__(self, *args, **kwargs):
        super(ChecklistForm, self).__init__(*args,**kwargs)
        self.fields['veiculo'] = forms.ModelChoiceField(
            label='Veículo:',
            queryset=Veiculo.objects.all(),
            empty_label="Selecione o veículo"
        )
        self.fields['veiculo'].widget.attrs.update({'class': ' form-control col-sm-8 mx-auto'})


class MotoristasForm(forms.ModelForm):
    class Meta:
        model = Motorista
        fields = ['nome', 'telefone', 'data_cadastro', 'documentos']

        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'xxxxxxxxxxx'}),
            'data_cadastro': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'dd/mm/aaaa'}),
            'documentos': forms.FileInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'nome': 'Nome:',
            'telefone': 'Telefone:',
            'data_cadastro': 'Data de cadastro:',
            'documentos': 'Documentos:'
        }


    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if len(nome) < 3:
            raise forms.ValidationError('O nome deve ter pelo menos 3 caracteres.')
        return nome

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')

        # Limita o tamanho do número de telefone
        if len(telefone) > 15:
            raise forms.ValidationError('O número de telefone deve ter no máximo 15 caracteres.')

        return telefone

    def clean_data_cadastro(self):
        data_cadastro = self.cleaned_data.get('data_cadastro')
        # Pode adicionar lógica de validação adicional conforme necessário
        if data_cadastro and data_cadastro > timezone.now().date():
            raise forms.ValidationError('A data de cadastro não pode ser no futuro.')
        return data_cadastro

    def clean_documentos(self):
        documentos = self.cleaned_data.get('documentos')

        # Verifica se é um arquivo PDF
        if documentos:
            if not documentos.name.endswith('.pdf'):
                raise forms.ValidationError('Por favor, envie um arquivo PDF.')

            # Verifica o tamanho do arquivo (por exemplo, limita a 5 MB)
            max_size = 5 * 1024 * 1024  # 5 MB
            if documentos.size > max_size:
                raise forms.ValidationError('O arquivo PDF não pode exceder 5 MB.')

        return documentos


class RotaForm(forms.ModelForm):
    class Meta:
        model = Rota
        fields = ['nome', 'turno', 'horario_saida', 'horario_retorno', 'motorista', 'veiculo', 'paradas']

        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'turno': forms.Select(attrs={'class': 'form-control'}),
            'horario_saida': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'horario_retorno': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'motorista': forms.Select(attrs={'class': 'form-control'}),
            'veiculo': forms.Select(attrs={'class': 'form-control'}),
            'paradas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

        labels = {
            'nome': 'Nome:',
            'turno': 'Turno:',
            'horario_saida': 'Horário de Saída:',
            'horario_retorno': 'Horário de Retorno:',
            'motorista': 'Motorista:',
            'veiculo': 'Veículo:',
            'paradas': 'Paradas:',
        }

    def clean_horario_saida(self):
        horario_saida = self.cleaned_data.get('horario_saida')
        # Adicione lógica de validação adicional conforme necessário
        return horario_saida

    def clean_horario_retorno(self):
        horario_retorno = self.cleaned_data.get('horario_retorno')
        # Adicione lógica de validação adicional conforme necessário
        return horario_retorno

    def clean(self):
        cleaned_data = super().clean()
        horario_saida = cleaned_data.get('horario_saida')
        horario_retorno = cleaned_data.get('horario_retorno')

        if horario_saida and horario_retorno and horario_saida >= horario_retorno:
            raise forms.ValidationError("O horário de retorno deve ser posterior ao horário de saída.")

        return cleaned_data

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if len(nome) < 3:
            raise forms.ValidationError("O nome da rota deve ter pelo menos 3 caracteres.")
        return nome

    def clean_turno(self):
        turno = self.cleaned_data.get('turno')
        if turno not in ['Manhã', 'Tarde', 'Noite']:
            raise forms.ValidationError("Selecione um turno válido.")
        return turno

    def clean_paradas(self):
        paradas = self.cleaned_data.get('paradas')
        if len(paradas.split(',')) < 2:
            raise forms.ValidationError("Forneça pelo menos duas paradas separadas por vírgula.")
        return paradas

    def __str__(self):
        return f"{self.nome} - {self.turno}"

class CombustivelForm(forms.ModelForm):
    class Meta:
        model = Combustivel
        fields = ['veiculo', 'data_cadastro', 'quantidade_abastecida', 'custo', 'comprovante_abastecimento']

        widgets = {
            'data_cadastro': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'dd/mm/aaaa'}),
            'quantidade_abastecida': forms.NumberInput(attrs={'class': 'form-control'}),
            'custo': forms.NumberInput(attrs={'class': 'form-control'}),
            'comprovante_abastecimento': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

        labels = {
            'data_cadastro': 'Data:',
            'quantidade_abastecida': 'Quantidade abastecida:',
            'custo': 'Custo:',
            'comprovante_abastecimento': 'Comprovante:',
        }

    def __init__(self, *args, **kwargs):
        super(CombustivelForm, self).__init__(*args, **kwargs)
        # Adiciona um campo de seleção para os modelos de veículos
        self.fields['veiculo'] = forms.ModelChoiceField(
            label='Veículo:',
            queryset=Veiculo.objects.all(),
            empty_label="Selecione o veículo",
            widget=forms.Select(attrs={'class': 'form-control col-sm-8 mx-auto'})
        )

    def clean_data_cadastro(self):
        data_cadastro = self.cleaned_data.get('data_cadastro')

        # Verifica se a data de cadastro está no futuro
        if data_cadastro and data_cadastro > timezone.now().date():
            raise forms.ValidationError('A data de cadastro não pode ser no futuro.')

        # Verifica se a data de cadastro está muito no passado (por exemplo, há 100 anos)
        if data_cadastro and data_cadastro < timezone.now().date() - timezone.timedelta(days=365 * 100):
            raise forms.ValidationError('A data de cadastro é muito antiga.')

        return data_cadastro

    def clean_quantidade_abastecida(self):
        quantidade_abastecida = self.cleaned_data.get('quantidade_abastecida')

        # Verifica se a quantidade abastecida é negativa
        if quantidade_abastecida and quantidade_abastecida < 0:
            raise forms.ValidationError('A quantidade abastecida não pode ser negativa.')

        return quantidade_abastecida

    def clean_custo(self):
        custo = self.cleaned_data.get('custo')

        # Verifica se o custo é negativo ou não é um número válido
        if custo is not None and (not isinstance(custo, (int, float)) or custo < 0):
            raise forms.ValidationError('O custo deve ser um número não negativo.')

        return custo


class DemandaForm(forms.ModelForm):
    class Meta:
        model = Demanda
        fields = ['veiculo', 'motorista', 'data', 'horario_saida', 'horario_retorno', 'descricao']

        widgets = {
            'veiculo': forms.Select(attrs={'class': 'form-control'}),
            'motorista': forms.Select(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'horario_saida': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'horario_retorno': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

        labels = {
            'veiculo': 'Veículo:',
            'motorista': 'Motorista:',
            'data': 'Data:',
            'horario_saida': 'Horário de Saída:',
            'horario_retorno': 'Horário de Retorno:',
            'descricao': 'Descrição:',
        }

    def clean_horario_saida(self):
        horario_saida = self.cleaned_data.get('horario_saida')
        # Adicione lógica de validação adicional conforme necessário
        return horario_saida

    def clean_horario_retorno(self):
        horario_retorno = self.cleaned_data.get('horario_retorno')
        # Adicione lógica de validação adicional conforme necessário
        return horario_retorno

    def clean_data(self):
        data = self.cleaned_data.get('data')
        return data

    def clean_descricao(self):
        descricao = self.cleaned_data.get('descricao')
        return descricao


class ViagemForm(forms.ModelForm):
    class Meta:
        model = Viagem
        fields = ['destino', 'veiculo', 'motorista', 'data_saida', 'data_retorno', 'descricao']

        widgets = {
            'destino': forms.TextInput(attrs={'class': 'form-control'}),
            'veiculo': forms.Select(attrs={'class': 'form-control'}),
            'motorista': forms.Select(attrs={'class': 'form-control'}),
            'data_saida': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_retorno': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

        labels = {
            'destino': 'Destino:',
            'veiculo': 'Veículo:',
            'motorista': 'Motorista:',
            'data_saida': 'Data de Saída:',
            'data_retorno': 'Data de Retorno:',
            'descricao': 'Descrição:',
        }

    def clean_data_retorno(self):
        data_retorno = self.cleaned_data.get('data_retorno')
        data_saida = self.cleaned_data.get('data_saida')

        if data_retorno and data_saida and data_retorno < data_saida:
            raise forms.ValidationError('A data de retorno não pode ser anterior à data de saída.')

        return data_retorno

    def clean_data_saida(self):
        data_saida = self.cleaned_data.get('data_saida')

        if data_saida and data_saida < timezone.now().date():
            raise forms.ValidationError('A data de saída não pode ser no passado.')

        return data_saida