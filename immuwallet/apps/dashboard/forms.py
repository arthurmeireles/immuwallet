# -*- coding: utf-8 -*-
import re

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Submit, HTML
from django import forms
from django.db.models import Q
from localflavor.br.forms import BRCPFField

from dashboard.models import Usuario, Perfil, Estabelecimento


class BRCPFFieldUnique(BRCPFField):
    """
    Extende a classe BRCPFField para forçar valores
    únicos para o CPF e também para sempre salvar apenas
    os números na base de dados sem pontos e hífem.
    Usado no UserRegistrationForm que não extende o ModelForm
    e por isso ignora o fato do campo cpf estar marcado como único.
    """

    def __init__(self, *args, **kwargs):
        super(BRCPFFieldUnique, self).__init__(*args, **kwargs)

    def clean(self, value):
        value = re.sub("[-\.]", "", value)

        if value == '00000000000':
            return value

        super(BRCPFFieldUnique, self).clean(value)

        return value


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

    def pesquisar(self, usuario):
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
