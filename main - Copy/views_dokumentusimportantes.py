from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main.decorators import allowed_users
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import *
from .forms import DokumentusimportantesForm
from main.utils import *


@login_required
@allowed_users(allowed_roles=['admin'])
def listadokumentusimportantes(request):
    dokumentusimportantes = Dokumentusimportantes.objects.all()
    first_three_dezen = dokumentusimportantes.order_by('-id')
    context = {
        "dokumentusimportantes": first_three_dezen
    }
    return render(request, "dokumentusimportantes/lista.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def inputdokumentusimportantes(request):
    if request.method == "POST":
        form = DokumentusimportantesForm(request.POST, request.FILES)
        if form.is_valid():
            dadus = form.save(commit=False)
            dadus.save()
            messages.success(request, "Dados Rejistu ho Susessu!")
            return redirect('listadokumentusimportantes')
    else:
        form = DokumentusimportantesForm()
    
    context = {
        'form': form
    }
    return render(request, "dokumentusimportantes/input.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def updatedokumentusimportantes(request, id):
    ide=decrypt_id(id)
    dokumentusimportantes = Dokumentusimportantes.objects.get(id=ide)
    if request.method == "POST":
        form = DokumentusimportantesForm(request.POST, request.FILES, instance=dokumentusimportantes)
        if form.is_valid():
            dadus = form.save(commit=False)
            dadus.save()
            messages.success(request, "Dadus Atualiza ho Susessu!")
            return redirect('listadokumentusimportantes')
    else:
        form = DokumentusimportantesForm(instance=dokumentusimportantes)
    
    context = {
        'form': form
    }
    return render(request, "dokumentusimportantes/update.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def hamosdokumentusimportantes(request, id):
    dokumentusimportantes = Dokumentusimportantes.objects.get(id=id)
    dokumentusimportantes.delete()
    messages.success(request, "Dadus Apaga Susessu!")
    return redirect('listadokumentusimportantes')

def show(request):
    dokumentusimportantes = Dokumentusimportantes.objects.all()
    first_three_dezen = dokumentusimportantes.order_by('-id')
    
    lingua = request.LANGUAGE_CODE
    if lingua == "en":
        first_three_dezen = dokumentusimportantes.filter(lingua__id=3).order_by('-id')
    elif lingua == "pt":
        first_three_dezen = dokumentusimportantes.filter(lingua__id=2).order_by('-id')
    elif lingua == "pt-br":
        first_three_dezen = dokumentusimportantes.filter(lingua__id=1).order_by('-id')
   
    context = {
        "dokumentusimportantes": first_three_dezen
    }
    return render(request, "dokumentusimportantes/show.html", context)
