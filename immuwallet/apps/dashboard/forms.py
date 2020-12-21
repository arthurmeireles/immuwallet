# -*- coding: utf-8 -*-

import csv

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Submit
from django import forms
from django.db import transaction

from dashboard.models import Municipio, Usuario, Perfil, Estabelecimento, Vacina, VacinaEstocada, VacinaAplicada, HoraMarcada, \
    HorarioFuncionamento


class Login(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class PesquisaUsuarioForm(forms.Form):
    first_name = forms.CharField(
        required=False,
        label="Primeiro nome",
        widget=forms.TextInput(),
    )
    second_name = forms.CharField(
        required=False,
        label="Último nome",
        widget=forms.TextInput(),
    )
    email = forms.CharField(
        required=False,
        label="Email",
        widget=forms.TextInput(),
    )

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario')
        super(PesquisaUsuarioForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        self.helper.layout = Layout(
            Div(
                Div(
                    Field('first_name', css_class="form-control"),
                    css_class="col-md-12 col-lg-4 col-xs-12"
                ),
                Div(
                    Field('second_name', css_class="form-control"),
                    css_class="col-md-12 col-lg-4 col-xs-12"
                ),
                Div(
                    Field('email', css_class="form-control"),
                    css_class="col-md-12 col-lg-4 col-xs-12"
                ),
                css_class="row"
            ),
            FormActions(Submit('submit', 'Pesquisar', css_class='pull-right')),
        )

    def pesquisar(self):
        usuario_list = Usuario.objects.all()

        if self.is_valid():
            if self.cleaned_data.get('first_name', None):
                usuario_list = usuario_list.filter(first_name__icontains=self.cleaned_data['first_name'])
            if self.cleaned_data.get('second_name', None):
                usuario_list = usuario_list.filter(last_name__icontains=self.cleaned_data['second_name'])
            if self.cleaned_data.get('email', None) and self.cleaned_data.get('email', None) != '':
                usuario_list = usuario_list.filter(email__icontains=self.cleaned_data['email'])
        else:
            usuario_list = Usuario.objects.none()

        return usuario_list


class UsuarioForm(forms.Form):
    first_name = forms.CharField(
        required=False,
        label="Primeiro nome",
        widget=forms.TextInput(),
    )
    last_name = forms.CharField(
        required=False,
        label="Último nome",
        widget=forms.TextInput(),
    )
    email = forms.EmailField(
        required=False,
        label="Email",
        widget=forms.TextInput(),
    )
    perfil = forms.ChoiceField(
        required=True,
        widget=forms.Select(),
        choices=Perfil.choices
    )
    estabelecimento = forms.ModelChoiceField(
        required=True,
        queryset=Estabelecimento.objects.all(),
        widget=forms.Select(),
        empty_label='Selecionar',
    )

    def __init__(self, *args, **kwargs):
        if 'usuario' in kwargs.keys():
            self.usuario = kwargs.pop("usuario")
        if 'instance' in kwargs.keys():
            self.instance = kwargs.pop("instance")

        super(UsuarioForm, self).__init__(*args, **kwargs)

        if self.instance:
            self.fields['first_name'].initial = self.instance.first_name
            self.fields['last_name'].initial = self.instance.last_name
            self.fields['email'].initial = self.instance.email
            if Perfil.objects.filter(usuario=self.instance).exists():
                self.fields['perfil'].initial = self.instance.perfil.tipo
                self.fields['estabelecimento'].initial = self.instance.perfil.estabelecimento

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        self.helper.layout = Layout(
            Div(
                Div(
                    Field('first_name', css_class="form-control"),
                    css_class="col-md-4 col-lg-4 col-xs-12"
                ),
                Div(
                    Field('last_name', css_class="form-control"),
                    css_class="col-md-4 col-lg-4 col-xs-12"
                ),
                Div(
                    Field('email', css_class="form-control"),
                    css_class="col-md-4 col-lg-4 col-xs-12"
                ),
                css_class="row"
            ),
            Div(
                Div(
                    Field('perfil', css_class="form-control"),
                    css_class="col-md-6 col-lg-6 col-xs-12"
                ),
                Div(
                    Field('estabelecimento', css_class="form-control"),
                    css_class="col-md-6 col-lg-6 col-xs-12"
                ),
                css_class="row"
            ),
            FormActions(Submit('submit', 'Salvar', css_class='pull-right')),
        )

    def save(self):
        tipo = self.cleaned_data.pop('perfil')
        estabelecimento = self.cleaned_data.pop('estabelecimento')

        for chave, valor in self.cleaned_data.items():
            setattr(self.instance, chave, valor)
        self.instance.save()

        if Perfil.objects.filter(usuario=self.instance).exists():
            perfil = self.instance.perfil
        else:
            perfil = Perfil(usuario=self.instance)

        perfil.tipo = tipo
        perfil.estabelecimento = estabelecimento
        perfil.save()

        return self.instance


class CadastrarUsuarioForm(forms.Form):
    username = forms.CharField(
        required=False,
        label="Nome de usuário",
        widget=forms.TextInput(),
    )
    first_name = forms.CharField(
        required=False,
        label="Primeiro nome",
        widget=forms.TextInput(),
    )
    last_name = forms.CharField(
        required=False,
        label="Último nome",
        widget=forms.TextInput(),
    )
    email = forms.EmailField(
        required=False,
        label="Email",
        widget=forms.TextInput(),
    )
    password = forms.CharField(
        required=False,
        label="Último nome",
        widget=forms.TextInput(),
    )

    def clean_email(self):
        if Usuario.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError('Email já existe!')
        return self.cleaned_data['email']

    def save(self):
        password = self.cleaned_data.pop('password')
        usuario = Usuario(**self.cleaned_data)
        usuario.set_password(password)
        usuario.save()

        return usuario


class VacinaEstocadaForm(forms.Form):
    vacina = forms.ModelChoiceField(
        required=True,
        queryset=Vacina.objects.all(),
        widget=forms.Select(),
        empty_label='Selecionar',
    )
    estabelecimento = forms.ModelChoiceField(
        required=True,
        queryset=Estabelecimento.objects.all(),
        widget=forms.Select(),
        empty_label='Selecionar',
    )
    quantidade = forms.IntegerField(required=True)
    data = forms.DateTimeField(required=True)

    def __init__(self, *args, **kwargs):
        super(VacinaEstocadaForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        self.helper.layout = Layout(
            Div(
                Div(
                    Field('vacina', css_class="form-control"),
                    css_class="col-md-4 col-lg-6 col-xs-12"
                ),
                Div(
                    Field('estabelecimento', css_class="form-control"),
                    css_class="col-md-4 col-lg-6 col-xs-12"
                ),
                css_class="row"
            ),
            Div(
                Div(
                    Field('quantidade', css_class="form-control"),
                    css_class="col-md-6 col-lg-6 col-xs-12"
                ),
                Div(
                    Field('data', css_class="form-control"),
                    css_class="col-md-6 col-lg-6 col-xs-12"
                ),
                css_class="row"
            ),
            FormActions(Submit('submit', 'Salvar', css_class='pull-right')),
        )

    def save(self):
        vacina = VacinaEstocada(**self.cleaned_data)
        vacina.save()

        return vacina


class VacinaAplicadaForm(forms.Form):
    vacina = forms.ModelChoiceField(
        required=True,
        queryset=Vacina.objects.all(),
        widget=forms.Select(),
        empty_label='Selecionar',
    )
    data = forms.DateField(required=True)

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop("usuario")

        super(VacinaAplicadaForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        self.helper.layout = Layout(
            Div(
                Div(
                    Field('vacina', css_class="form-control"),
                    css_class="col-md-4 col-lg-6 col-xs-12"
                ),
                Div(
                    Field('data', css_class="form-control"),
                    css_class="col-md-4 col-lg-6 col-xs-12"
                ),
                css_class="row"
            ),
            FormActions(Submit('submit', 'Salvar', css_class='pull-right')),
        )

    def save(self):
        vacina = VacinaAplicada(paciente=self.usuario, **self.cleaned_data)
        vacina.save()

        return vacina


class HoraMarcadaForm(forms.Form):
    vacina = forms.ModelChoiceField(
        required=True,
        queryset=Vacina.objects.all(),
        widget=forms.Select(),
        empty_label='Selecionar',
    )
    estabelecimento = forms.ModelChoiceField(
        required=True,
        queryset=Estabelecimento.objects.all(),
        widget=forms.Select(),
        empty_label='Selecionar',
    )
    data = forms.DateTimeField(required=True)

    def __init__(self, *args, **kwargs):
        if 'usuario' in kwargs.keys():
            self.usuario = kwargs.pop("usuario")

        super(HoraMarcadaForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        self.helper.layout = Layout(
            Div(
                Div(
                    Field('vacina', css_class="form-control"),
                    css_class="col-md-4 col-lg-4 col-xs-12"
                ),
                Div(
                    Field('estabelecimento', css_class="form-control"),
                    css_class="col-md-4 col-lg-4 col-xs-12"
                ),
                Div(
                    Field('data', css_class="form-control"),
                    css_class="col-md-4 col-lg-4 col-xs-12"
                ),
                css_class="row"
            ),
            FormActions(Submit('submit', 'Salvar', css_class='pull-right')),
        )

    def clean_data(self):
        try:
            estabelecimento = self.cleaned_data['estabelecimento']
            data = self.cleaned_data['data']
            vacina = self.cleaned_data['vacina']
            estabelecimento.horario_atendimento_disponivel(data, vacina)
        except Exception as e:
            raise forms.ValidationError(e)
        return self.cleaned_data['data']

    def save(self):

        hora_marcada = HoraMarcada(**self.cleaned_data)
        hora_marcada.status = HoraMarcada.MARCADO
        hora_marcada.paciente = self.usuario
        hora_marcada.save()

        hora_marcada.save()


class HorarioFuncionamentoForm(forms.Form):
    dia_semana = forms.ChoiceField(
        required=False,
        widget=forms.Select(),
        choices=HorarioFuncionamento.DIAS
    )
    hora_abre = forms.TimeField(required=True)
    hora_fecha = forms.TimeField(required=True)
    data = forms.DateField(required=False)
    estabelecimento = forms.ModelChoiceField(
        required=True,
        queryset=Estabelecimento.objects.all(),
        widget=forms.Select(),
        empty_label='Selecionar',
    )

    def __init__(self, *args, **kwargs):
        if 'usuario' in kwargs.keys():
            self.usuario = kwargs.pop("usuario")
        self.instance = kwargs.pop("instance", None)

        super(HorarioFuncionamentoForm, self).__init__(*args, **kwargs)

        if self.usuario and Perfil.objects.filter(usuario=self.usuario).exists():
            self.fields['estabelecimento'].initial = self.usuario.perfil.estabelecimento
        if self.instance:
            self.fields['dia_semana'].initial = self.instance.dia_semana
            self.fields['hora_abre'].initial = self.instance.hora_abre
            self.fields['hora_fecha'].initial = self.instance.hora_fecha
            self.fields['data'].initial = self.instance.data
            self.fields['estabelecimento'].initial = self.instance.estabelecimento

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        self.helper.layout = Layout(
            Div(
                Div(
                    Field('dia_semana', css_class="form-control"),
                    css_class="col-md-4 col-lg-4 col-xs-12"
                ),
                Div(
                    Field('hora_abre', css_class="form-control"),
                    css_class="col-md-4 col-lg-4 col-xs-12"
                ),
                Div(
                    Field('hora_fecha', css_class="form-control"),
                    css_class="col-md-4 col-lg-4 col-xs-12"
                ),
                css_class="row"
            ),
            Div(
                Div(
                    Field('data', css_class="form-control"),
                    css_class="col-md-6 col-lg-6 col-xs-12"
                ),
                Div(
                    Field('estabelecimento', css_class="form-control"),
                    css_class="col-md-6 col-lg-6 col-xs-12"
                ),
                css_class="row"
            ),
            FormActions(Submit('submit', 'Salvar', css_class='pull-right')),
        )

    def clean(self):
        if self.cleaned_data['data'] is not None:
            self.cleaned_data['dia_semana'] = None
        return self.cleaned_data

    def save(self):
        if self.instance:
            horario_funcionamento = self.instance
        else:
            horario_funcionamento = HorarioFuncionamento()

        for chave, valor in self.cleaned_data.items():
            setattr(horario_funcionamento, chave, valor)
        horario_funcionamento.save()

        return horario_funcionamento


class EstabelecimentoForm(forms.Form):
    arquivo = forms.FileField(required=True, label='Arquivo')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(EstabelecimentoForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        self.helper.layout = Layout(
            Div(
                Div(
                    Field('arquivo', css_class="form-control"),
                    css_class="col-md-12 col-lg-12 col-xs-12"
                ),
                css_class="row",
            ),
            FormActions(Submit('submit', 'Salvar', css_class='pull-right')),
        )

    def save(self):
        try:
            string = self.cleaned_data['arquivo'].read().decode('utf8').splitlines()
            reader = csv.DictReader(string)
            with transaction.atomic():
                municipio = Municipio.objects.first()
                for linha in reader:
                    Estabelecimento.objects.update_or_create(
                        cnes=linha['CO_CNES'],
                        defaults={
                            'nome': linha['NO_RAZAO_SOCIAL'],
                            'municipio': municipio
                        }
                    )
        except Exception as error:
            print('erro arquivo', error)
            raise forms.ValidationError(u'Arquivo inválido.')


class RelatorioForm(forms.Form):
    vacina = forms.ModelChoiceField(
        required=False,
        queryset=Vacina.objects.all(),
        widget=forms.Select(),
        empty_label='Selecionar',
    )
    estabelecimento = forms.ModelChoiceField(
        required=False,
        queryset=Estabelecimento.objects.all(),
        widget=forms.Select(),
        empty_label='Selecionar',
    )

    def __init__(self, *args, **kwargs):
        super(RelatorioForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        self.helper.layout = Layout(
            Div(
                Div(
                    Field('vacina', css_class="form-control"),
                    css_class="col-md-4 col-lg-4 col-xs-12"
                ),
                Div(
                    Field('estabelecimento', css_class="form-control"),
                    css_class="col-md-4 col-lg-4 col-xs-12"
                ),
                css_class="row"
            ),
            FormActions(Submit('submit', 'Download', css_class='pull-right')),
        )
