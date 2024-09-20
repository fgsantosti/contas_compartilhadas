from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Grupo, Renda, Gasto
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import GrupoForm, RendaForm, GastoForm, AdicionarMembroForm, FiltrarGastosForm
from django.db.models import Sum


from django.contrib.auth import authenticate, login, logout

def index(request):
    return render(request, 'financeiro/index.html',{})

def index(request):
    return render(request, 'financeiro/index.html',{})

def login_view(request):
    return render(request, 'financeiro/login.html',{})

def logout_view(request):
    logout(request)

def autenticar_usuario(request):
    username = request.POST['username']
    password = request.POST['password']
    #user = authenticate(username="fgs", password="123456")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        grupos = request.user.grupos.all()  # Grupos onde o usuário é membro
        return render(request, 'financeiro/home.html', {'grupos': grupos})
    else:
        return render(request, 'financeiro/index.html',{})

@login_required
def criar_grupo(request):
    if request.method == 'POST':
        form = GrupoForm(request.POST)
        if form.is_valid():
            grupo = form.save(commit=False)
            grupo.criador = request.user
            grupo.save()
            grupo.membros.add(request.user)  # Adiciona o criador como membro
            return redirect('detalhes_grupo', grupo.id)
    else:
        form = GrupoForm()
    return render(request, 'financeiro/criar_grupo.html', {'form': form})

@login_required
def adicionar_renda(request, grupo_id):
    grupo = get_object_or_404(Grupo, id=grupo_id)
    if request.method == 'POST':
        form = RendaForm(request.POST)
        if form.is_valid():
            renda = form.save(commit=False)
            renda.usuario = request.user
            renda.grupo = grupo
            renda.save()
            return redirect('detalhes_grupo', grupo_id)
    else:
        form = RendaForm()
    return render(request, 'financeiro/adicionar_renda.html', {'form': form, 'grupo': grupo})

@login_required
def adicionar_gasto(request, grupo_id):
    grupo = get_object_or_404(Grupo, id=grupo_id)
    if request.method == 'POST':
        form = GastoForm(request.POST)
        if form.is_valid():
            gasto = form.save(commit=False)
            gasto.usuario = request.user
            gasto.grupo = grupo
            gasto.save()
            return redirect('detalhes_grupo', grupo_id)
    else:
        form = GastoForm()
    return render(request, 'financeiro/adicionar_gasto.html', {'form': form, 'grupo': grupo})

@login_required
def detalhes_grupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, id=grupo_id)
    rendas = Renda.objects.filter(grupo=grupo)
    gastos = Gasto.objects.filter(grupo=grupo)
    return render(request, 'financeiro/detalhes_grupo.html', {'grupo': grupo, 'rendas': rendas, 'gastos': gastos})


@login_required
def adicionar_membro(request, grupo_id):
    grupo = get_object_or_404(Grupo, id=grupo_id)

    if request.user != grupo.criador:
        messages.error(request, 'Apenas o criador do grupo pode adicionar membros.')
        return redirect('detalhes_grupo', grupo_id)

    if request.method == 'POST':
        form = AdicionarMembroForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                usuario = User.objects.get(email=email)
                if usuario in grupo.membros.all():
                    messages.warning(request, 'Este usuário já é membro do grupo.')
                else:
                    grupo.membros.add(usuario)
                    messages.success(request, f'{usuario.username} foi adicionado ao grupo.')
            except User.DoesNotExist:
                messages.error(request, 'Usuário com este e-mail não foi encontrado.')
            return redirect('detalhes_grupo', grupo_id)
    else:
        form = AdicionarMembroForm()

    return render(request, 'financeiro/adicionar_membro.html', {'form': form, 'grupo': grupo})


@login_required
def home(request):
    #grupos = request.user.grupos.all()  # Grupos onde o usuário é membro
    grupos = Grupo.objects.filter(criador=request.user)  # Grupos criados pelo usuário
    return render(request, 'financeiro/home.html', {'grupos': grupos})



@login_required
def listar_gastos_por_data(request, grupo_id):
    grupo = get_object_or_404(Grupo, id=grupo_id)
    
    gastos = Gasto.objects.filter(grupo=grupo)  # Inicialmente todos os gastos do grupo
    total_gastos = 0  # Variável para armazenar a soma dos gastos filtrados
    form = FiltrarGastosForm()

    if request.method == 'POST':
        form = FiltrarGastosForm(request.POST)
        if form.is_valid():
            data_inicio = form.cleaned_data['data_inicio']
            data_fim = form.cleaned_data['data_fim']
            
            # Filtrando os gastos no intervalo de data
            gastos = gastos.filter(data__range=[data_inicio, data_fim])
            
            # Somando os gastos
            total_gastos = gastos.aggregate(Sum('valor'))['valor__sum'] or 0
    
    return render(request, 'financeiro/listar_gastos.html', {
        'form': form, 
        'gastos': gastos, 
        'total_gastos': total_gastos, 
        'grupo': grupo
    })
