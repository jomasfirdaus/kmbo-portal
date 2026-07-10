from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import RegistuVoluntariu
from .forms import RegistuVoluntariuForm
from main.utils import decrypt_id
from main.decorators import allowed_users

@login_required
@allowed_users(allowed_roles=['admin'])
def listaregistuvoluntariu(request):
    registuvoluntariu = RegistuVoluntariu.objects.all().order_by('-id')
    context = {
        "registuvoluntariu": registuvoluntariu
    }
    return render(request, "registuvoluntariu/lista.html", context)


@login_required
@allowed_users(allowed_roles=['admin'])
def inputregistuvoluntariu(request):
    if request.method == "POST":
        form = RegistuVoluntariuForm(request.POST, request.FILES)
        if form.is_valid():
            dadus = form.save(commit=False)
            dadus.save()
            messages.success(request, "Dados Rejistu ho Susessu!")
            return redirect('listaregistuvoluntariu')
    else:
        form = RegistuVoluntariuForm()
    
    context = {
        'form': form
    }
    return render(request, "registuvoluntariu/input.html", context)


@login_required
@allowed_users(allowed_roles=['admin'])
def updateregistuvoluntariu(request, id):
    ide = decrypt_id(id)
    registuvoluntariu = get_object_or_404(RegistuVoluntariu, id=ide)
    if request.method == "POST":
        form = RegistuVoluntariuForm(request.POST, request.FILES, instance=registuvoluntariu)
        if form.is_valid():
            dadus = form.save(commit=False)
            dadus.save()
            messages.success(request, "Dadus Atualiza ho Susessu!")
            return redirect('listaregistuvoluntariu')
    else:
        form = RegistuVoluntariuForm(instance=registuvoluntariu)
    
    context = {
        'form': form
    }
    return render(request, "registuvoluntariu/update.html", context)


@login_required
@allowed_users(allowed_roles=['admin'])
def hamosregistuvoluntariu(request, id):
    ide = decrypt_id(id)
    registuvoluntariu = get_object_or_404(RegistuVoluntariu, id=ide)
    registuvoluntariu.delete()
    messages.success(request, "Dadus Apaga ho Susessu!")
    return redirect('listaregistuvoluntariu')



def showregistuvoluntariu(request):
    registuvoluntariu = RegistuVoluntariu.objects.all().order_by('-id')
    lingua = request.LANGUAGE_CODE
    if lingua == "en":
        registuvoluntariu = registuvoluntariu.filter(lingua__id=3)
    elif lingua == "pt":
        registuvoluntariu = registuvoluntariu.filter(lingua__id=2)
    elif lingua == "pt-br":
        registuvoluntariu = registuvoluntariu.filter(lingua__id=1)
    
    context = {
        "registuvoluntariu": registuvoluntariu
    }
    return render(request, "registuvoluntariu/show.html", context)
