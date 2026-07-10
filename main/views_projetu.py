from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import *
from .forms import ProjetuForm
from main.utils import *
from main.decorators import allowed_users

@login_required
@allowed_users(allowed_roles=['admin'])
def listaprojetu(request):
    projetu = Projetu.objects.all()
    first_three_dezen = projetu.order_by('-id')
    context = {
        "projetu": first_three_dezen
    }
    return render(request, "projetu/lista.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def inputprojetu(request):
    if request.method == "POST":
        form = ProjetuForm(request.POST, request.FILES)
        if form.is_valid():
            dadus = form.save(commit=False)
            dadus.save()
            messages.success(request, "Dados Rejistu ho Susessu!")
            return redirect('listaprojetu')
    else:
        form = ProjetuForm()
    
    context = {
        'form': form
    }
    return render(request, "projetu/input.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def updateprojetu(request, id):
    ide=decrypt_id(id)
    projetu = Projetu.objects.get(id=ide)
    if request.method == "POST":
        form = ProjetuForm(request.POST, request.FILES, instance=projetu)
        if form.is_valid():
            dadus = form.save(commit=False)
            dadus.save()
            messages.success(request, "Dadus Atualiza ho Susessu!")
            return redirect('listaprojetu')
    else:
        form = ProjetuForm(instance=projetu)
    
    context = {
        'form': form
    }
    return render(request, "projetu/update.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def hamosprojetu(request, id):
    ide=decrypt_id(id)
    projetu = Projetu.objects.get(id=ide)
    projetu.delete()
    messages.success(request, "Dadus Apaga Susessu!")
    return redirect('listaprojetu')

def show(request):
    lingua = request.LANGUAGE_CODE  # Hakarak hetan lingua atu filtra
    lingua_id = None

    if lingua == "en":
        lingua_id = 3
    elif lingua == "pt":
        lingua_id = 2
    elif lingua == "tet":
        lingua_id = 1

    if lingua_id:
        projetu_all = Projetu.objects.filter(lingua__id=lingua_id)
    else:
        projetu_all = Projetu.objects.all()

    # Filtra projetu baseia ba status
    prosesu = projetu_all.filter(status='prosesu').order_by('-id')
    kompri = projetu_all.filter(status='kumpri').order_by('-id')

    context = {
        'prosesu': prosesu,
        'kompri': kompri,
    }
    return render(request, "projetu/show.html", context)
