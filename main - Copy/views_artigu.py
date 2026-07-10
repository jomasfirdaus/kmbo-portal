from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main.decorators import allowed_users
from django.contrib import messages
from .models import Artigu
from .forms import ArtiguForm
from main.utils import *


@login_required
@allowed_users(allowed_roles=['admin'])
def listaartigu(request):
    artigu = Artigu.objects.all().order_by('-id')
    context = {
        "artigu": artigu
    }
    return render(request, "artigu/lista.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def inputartigu(request):
    if request.method == 'POST':
        formulariu = ArtiguForm(request.POST, request.FILES)
        if formulariu.is_valid():
            dadus = formulariu.save(commit=False)
            dadus.save()
            messages.success(request, "Dados Rejistu ho Susessu..!")
            return redirect('listaartigu')
    else:
        formulariu = ArtiguForm()

    context = {
        'form': formulariu,
        'asaun': 'rejistu'
    }
    return render(request, "artigu/input.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def updateartigu(request, id):
    ide = decrypt_id(id)
    artigu = Artigu.objects.get(id=ide)
    if request.method == 'POST':
        formulariu = ArtiguForm(request.POST, request.FILES, instance=artigu)
        if formulariu.is_valid():
            dadus = formulariu.save(commit=False)
            dadus.save()
            messages.success(request, "Dadus Atualiza ho Susessu..!")
            return redirect('listaartigu')
    else:
        formulariu = ArtiguForm(instance=artigu)

    context = {
        'form': formulariu,
        'asaun': 'edit'
    }
    return render(request, "artigu/input.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def hamosartigu(request, id):
    artigu = Artigu.objects.get(id=id)
    artigu.delete()
    messages.success(request, "Dadus Apaga Susessu..!")
    return redirect('listaartigu')

def showartigu(request):
    artigu = Artigu.objects.all()
    lingua = request.LANGUAGE_CODE  # ka get_language()
    
    if lingua == "en":
        artigu = artigu.filter(lingua__id=3)
    elif lingua == "pt":
        artigu = artigu.filter(lingua__id=2)
    elif lingua == "pt-br":
        artigu = artigu.filter(lingua__id=1)

    return render(request, "artigu/show.html", {"artigu": artigu})