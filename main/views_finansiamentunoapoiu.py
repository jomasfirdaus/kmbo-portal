from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main.decorators import allowed_users
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import *
from .forms import FinansiamentunoapoiuForm
from main.utils import *


@login_required
@allowed_users(allowed_roles=['admin'])
def listafinansiamentunoapoiu(request):
    finansiamentunoapoiu = Finansiamentunoapoiu.objects.all()
    first_three_dezen = finansiamentunoapoiu.order_by('-id')
    context = {
        "finansiamentunoapoiu": first_three_dezen
    }
    return render(request, "finansiamentunoapoiu/lista.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def inputfinansiamentunoapoiu(request):
    if request.method == "POST":
        form = FinansiamentunoapoiuForm(request.POST, request.FILES)
        if form.is_valid():
            dadus = form.save(commit=False)
            dadus.save()
            messages.success(request, "Dados Rejistu ho Susessu!")
            return redirect('listafinansiamentunoapoiu')
    else:
        form = FinansiamentunoapoiuForm()
    
    context = {
        'form': form
    }
    return render(request, "finansiamentunoapoiu/input.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def updatefinansiamentunoapoiu(request, id):
    ide=decrypt_id(id)
    finansiamentunoapoiu = Finansiamentunoapoiu.objects.get(id=ide)
    if request.method == "POST":
        form = FinansiamentunoapoiuForm(request.POST, request.FILES, instance=finansiamentunoapoiu)
        if form.is_valid():
            dadus = form.save(commit=False)
            dadus.save()
            messages.success(request, "Dadus Atualiza ho Susessu!")
            return redirect('listafinansiamentunoapoiu')
    else:
        form = FinansiamentunoapoiuForm(instance=finansiamentunoapoiu)
    
    context = {
        'form': form
    }
    return render(request, "finansiamentunoapoiu/update.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def hamosfinansiamentunoapoiu(request, id):
    ide=decrypt_id(id)
    finansiamentunoapoiu = Finansiamentunoapoiu.objects.get(id=ide)
    finansiamentunoapoiu.delete()
    messages.success(request, "Dadus Apaga Susessu!")
    return redirect('listafinansiamentunoapoiu')

def show(request):
    finansiamentunoapoiu = Finansiamentunoapoiu.objects.all()
    first_three_dezen = finansiamentunoapoiu.order_by('-id')
    
    lingua = request.LANGUAGE_CODE
    if lingua == "en":
        first_three_dezen = finansiamentunoapoiu.filter(lingua__id=3).order_by('-id')
    elif lingua == "pt":
        first_three_dezen = finansiamentunoapoiu.filter(lingua__id=2).order_by('-id')
    elif lingua == "pt-br":
        first_three_dezen = finansiamentunoapoiu.filter(lingua__id=1).order_by('-id')
   
    context = {
        "finansiamentunoapoiu": first_three_dezen
    }
    return render(request, "finansiamentunoapoiu/show.html", context)
