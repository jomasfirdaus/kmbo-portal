from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main.decorators import allowed_users
from django.contrib import messages
from .models import Atividade
from .forms import AtividadeForm
from main.utils import *

@login_required
@allowed_users(allowed_roles=['admin'])
def listaatividade(request):
    atividade = Atividade.objects.all().order_by('-id')
    context = {
        "atividade": atividade
    }
    return render(request, "atividade/lista.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def inputatividade(request):
    if request.method == 'POST':
        formulariu = AtividadeForm(request.POST, request.FILES)
        if formulariu.is_valid():
            dadus = formulariu.save(commit=False)
            dadus.save()
            messages.success(request, "Dados Rejistu ho Susessu..!")
            return redirect('listaatividade')
    else:
        formulariu = AtividadeForm()

    context = {
        'form': formulariu,
        'asaun': 'rejistu'
    }
    return render(request, "atividade/input.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def updateatividade(request, id):
    ide = decrypt_id(id)
    atividade = Atividade.objects.get(id=ide)
    if request.method == 'POST':
        formulariu = AtividadeForm(request.POST, request.FILES, instance=atividade)
        if formulariu.is_valid():
            dadus = formulariu.save(commit=False)
            dadus.save()
            messages.success(request, "Dadus Atualiza ho Susessu..!")
            return redirect('listaatividade')
    else:
        formulariu = AtividadeForm(instance=atividade)

    context = {
        'form': formulariu,
        'asaun': 'edit'
    }
    return render(request, "atividade/input.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def hamosatividade(request, id):
    atividade = Atividade.objects.get(id=id)
    atividade.delete()
    messages.success(request, "Dadus Apaga Susessu..!")
    return redirect('listaatividade')


def showatividade(request):
    lingua = request.LANGUAGE_CODE  # Hakarak hetan lingua
    if lingua == "en":
        atividade = Atividade.objects.filter(lingua__id=3)
    elif lingua == "pt":
        atividade = Atividade.objects.filter(lingua__id=2)
    elif lingua == "tet":
        atividade = Atividade.objects.filter(lingua__id=1)
    else:
        atividade = Atividade.objects.all()  # fallback

    return render(request, "atividade/show.html", {"atividade": atividade})

