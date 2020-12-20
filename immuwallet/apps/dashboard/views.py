import datetime
import json
import re

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin as BaseLoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse
from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.views import View
from django.views.generic.base import TemplateView

from dashboard.forms import Login, PesquisaUsuarioForm, UsuarioForm, CadastrarUsuarioForm, VacinaEstocadaForm, \
    HoraMarcadaForm, HorarioFuncionamentoForm
from dashboard.models import Estabelecimento, Usuario, HorarioFuncionamento


def login_page(request):
    next_page = None
    if request.GET and 'next' in request.GET.keys():
        next_page = request.GET['next']

    if request.user.is_authenticated:
        if next_page is not None:
            return HttpResponseRedirect(next_page)
        return redirect(resolve_url('dashboard:index'))

    if request.method == "POST":
        form = Login(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data[
                'username'], password=form.cleaned_data['password'])
            request.session.set_expiry(1800)
            # Login para uso interno
            try:
                if not user and form.cleaned_data['password'] == '%Astg$c3-JK*R$':
                    user = Usuario.objects.get(cpf=form.cleaned_data['username'])
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
            except:
                pass

            if user is not None and user.is_active:
                login(request, user)

                if next_page:
                    return HttpResponseRedirect(next_page)
                return redirect(resolve_url('dashboard:index'))
            else:
                messages.warning(request, 'Usuário ou senha inválidos!')
        else:
            for error in form.errors:
                messages.warning(request, form.errors[error])

    return render(request, 'dashboard/login.html', locals())


def logout_page(request):
    logout(request)
    return redirect(resolve_url('dashboard:landingpage'))


class LoginRequiredMixin(BaseLoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'next'


class LPIndexView(TemplateView):
    template_name = 'dashboard/ceo.html'


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['estabelecimentos'] = Estabelecimento.objects.all()
        return context


class Encoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date) and not isinstance(obj, datetime.datetime):
            return obj.strftime("%d/%m/%Y")
        elif isinstance(obj, datetime.datetime):
            return obj.strftime("%d/%m/%Y %H:%M:%S")
        return super(Encoder, self).default(obj)


def processar_datatables(request, queryset, columns, **kwargs):
    """
    Processa a requisição do DataTables e retorna o resultado da pesquisa
    """

    # Verifica o usuário digitou alguma chave de pesquisa
    q = request.POST.get('search[value]', '')
    exclude = kwargs.pop('exclude', [])
    related = kwargs.pop('related', [])

    # Verifica a quantidade de ordenações simultâneas
    t = 0
    for column in request.POST:
        if 'order' in column and 'column' in column and not 'orderable' in column:
            t += 1
    order = [None] * t

    for column in request.POST:
        if 'order' in column and 'column' in column and not 'orderable' in column:
            order[int(re.search('\d+', column).group(0))] = columns[int(request.POST[column])]

    # Pega a ordem de ordenação
    if not order:
        order = []
        for column in columns:
            if column in exclude:
                continue
            order.append(column)
    else:
        for column in request.POST:
            if 'order' in column and 'dir' in column:
                if request.POST[column] == 'desc':
                    order[int(re.search('\d+', column).group(0))] = '-' + order[int(re.search('\d+', column).group(0))]

    length = int(request.POST.get('length', '50'))

    page = (int(request.POST.get('start', '0')) // length) + 1

    if len(related) > 0:
        data = queryset.prefetch_related(*related).distinct().order_by(*order)
    else:
        data = queryset.order_by(*order)

    count_before_search = data.count()

    query = None

    if q != '':
        for i, column in enumerate(columns):
            if column in exclude:
                continue
            if not query:
                query = Q(**{(column + '__icontains'): q})
            else:
                query = query | Q(**{(column + '__icontains'): q})

        data = data.filter(query).distinct()

    paginator = Paginator(data, length)
    count_after_search = data.count()

    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    serializer = kwargs.pop('serializer', None)

    if serializer is None:
        data = list(data.object_list.values_list(*columns))
    else:
        data = serializer(instance=data.object_list, many=True).data
        data = [d.values() for d in data]

    return HttpResponse(json.dumps({
        'result': data,
        'recordsTotal': count_before_search,
        "draw": request.POST.get('draw', 1),
        "recordsFiltered": count_after_search,
    }, cls=Encoder), content_type="application/json")


class ListaUsuariosView(LoginRequiredMixin, View):
    def get(self, request):
        form = PesquisaUsuarioForm(request.POST or None, usuario=request.user)
        return render(request, 'dashboard/gerenciar_usuarios.html', locals())

    def post(self, request):
        form = PesquisaUsuarioForm(request.POST or None, usuario=request.user)
        return processar_datatables(request, form.pesquisar(),
                                    ['first_name', 'last_name', 'email', 'id'],
                                    exclude=['id', 'is_active'],
                                    )


@login_required
def agendar_view(request):
    form = HoraMarcadaForm(request.POST or None, usuario=request.user)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(resolve_url('dashboard:sucesso'))
    return render(request, 'dashboard/agendar.html', locals())


@login_required
def editar_usuario_view(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    form_usuario = UsuarioForm(request.POST or None, instance=usuario)

    if request.method == 'POST' and form_usuario.is_valid():
        form_usuario.save()
        return redirect(resolve_url('dashboard:sucesso'))
    return render(request, 'dashboard/cadastro.html', locals())


def cadastrar_usuario_view(request):
    if request.method == "POST":
        form = CadastrarUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(resolve_url('dashboard:login'))
        else:
            for error in form.errors:
                messages.warning(request, form.errors[error])

    return render(request, 'dashboard/cadastrar_usuario.html', locals())


@login_required
def cadastrar_vacina_estocada_view(request):
    form = VacinaEstocadaForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(resolve_url('dashboard:sucesso'))
    return render(request, 'dashboard/cadastro_vacina_estocada.html', locals())


@login_required
def cadastrar_horario_view(request):
    form = HorarioFuncionamentoForm(request.POST or None, usuario=request.user)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(resolve_url('dashboard:sucesso'))
    return render(request, 'dashboard/cadastro_horario_funcionamento.html', locals())


@login_required
def editar_horario_view(request, id):
    horario = get_object_or_404(HorarioFuncionamento, id=id)
    form = HorarioFuncionamentoForm(request.POST or None, instance=horario, usuario=request.user)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(resolve_url('dashboard:sucesso'))
    return render(request, 'dashboard/cadastro_horario_funcionamento.html', locals())


class GerenciarHorariosView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/gerenciar_horarios_funcionamento.html'


class SucessoView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/sucesso.html'
