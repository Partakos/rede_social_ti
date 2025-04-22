from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Perfil, Publicacao, Amizade
from .forms import PerfilForm, PublicacaoForm

def inicio(request):
    if request.user.is_authenticated:
        try:
            perfil = request.user.perfil
        except Perfil.DoesNotExist:
            return redirect('editar_perfil')
            
        publicacoes = Publicacao.objects.filter(
            autor__in=[amizade.destinatario for amizade in 
                      Amizade.objects.filter(remetente=perfil, status='aceito')] +
                     [amizade.remetente for amizade in 
                      Amizade.objects.filter(destinatario=perfil, status='aceito')] +
                     [perfil]
        ).order_by('-data_publicacao')
    else:
        publicacoes = Publicacao.objects.all().order_by('-data_publicacao')[:10]
    
    return render(request, 'core/inicio.html', {
        'publicacoes': publicacoes,
    })

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('editar_perfil')
    else:
        form = UserCreationForm()
    return render(request, 'core/registro.html', {'form': form})

@login_required
def editar_perfil(request):
    perfil, created = Perfil.objects.get_or_create(usuario=request.user)
    
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('ver_perfil', perfil_id=perfil.id)
    else:
        form = PerfilForm(instance=perfil)
    
    return render(request, 'core/editar_perfil.html', {'form': form})

@login_required
def ver_perfil(request, perfil_id):
    perfil = get_object_or_404(Perfil, id=perfil_id)
    publicacoes = Publicacao.objects.filter(autor=perfil).order_by('-data_publicacao')
    
    # Verificar status de amizade
    amizade_status = None
    if request.user.is_authenticated and request.user != perfil.usuario:
        try:
            solicitacao = Amizade.objects.get(
                remetente=request.user.perfil,
                destinatario=perfil
            )
            amizade_status = solicitacao.status
        except Amizade.DoesNotExist:
            try:
                solicitacao = Amizade.objects.get(
                    remetente=perfil,
                    destinatario=request.user.perfil
                )
                amizade_status = solicitacao.status
            except Amizade.DoesNotExist:
                pass
    
    return render(request, 'core/perfil.html', {
        'perfil': perfil,
        'publicacoes': publicacoes,
        'amizade_status': amizade_status,
    })

@login_required
def solicitar_amizade(request, perfil_id):
    destinatario = get_object_or_404(Perfil, id=perfil_id)
    remetente = request.user.perfil
    
    if destinatario != remetente:
        Amizade.objects.get_or_create(
            remetente=remetente,
            destinatario=destinatario,
            defaults={'status': 'pendente'}
        )
        messages.success(request, 'Solicitação de amizade enviada!')
    
    return redirect('core/ver_perfil', perfil_id=perfil_id)

@login_required
def aceitar_amizade(request, solicitacao_id):
    solicitacao = get_object_or_404(Amizade, id=solicitacao_id, destinatario=request.user.perfil)
    solicitacao.status = 'aceito'
    solicitacao.save()
    messages.success(request, 'Amizade aceita!')
    return redirect('ver_perfil', perfil_id=solicitacao.remetente.id)

@login_required
def criar_publicacao(request):
    if request.method == 'POST':
        form = PublicacaoForm(request.POST, request.FILES)
        if form.is_valid():
            publicacao = form.save(commit=False)
            publicacao.autor = request.user.perfil
            publicacao.save()
            messages.success(request, 'Publicação criada com sucesso!')
            return redirect('inicio')
    else:
        form = PublicacaoForm()
    
    return render(request, 'core/criar_publicacao.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inicio')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'core/login.html')

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('editar_perfil')
    else:
        form = UserCreationForm()
    return render(request, 'core/registro.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('inicio')