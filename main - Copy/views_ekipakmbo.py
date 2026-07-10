from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main.decorators import allowed_users
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import EkipakmboForm
from django.contrib import messages
from main.utils import *
@login_required
@allowed_users(allowed_roles=['admin'])
def listaekipakmbo(request):
    ekipakmbo = Ekipakmbo.objects.all()
    first_mensajenhusikordenador = ekipakmbo.order_by('-id')
    context = {
        "ekipakmbo" : first_mensajenhusikordenador
        }
    return render(request, "ekipakmbo/lista.html", context)
@login_required
@allowed_users(allowed_roles=['admin'])
def inputekipakmbo(request):
    if request.method == 'POST':
        forms = EkipakmboForm(request.POST, request.FILES)
        if forms.is_valid():
            dadus = forms.save(commit=False)
            dadus.save()
            messages.success(request, "Dados Rejistu ho Susessu..!")
            return redirect('listaekipakmbo')
    else:
        forms = EkipakmboForm()
    
    context = {'form': forms}
    return render(request, "ekipakmbo/input.html", context)



@login_required
@allowed_users(allowed_roles=['admin'])
def updateekipakmbo(request, id):
    ide=decrypt_id(id)
    ekipakmbo = Ekipakmbo.objects.get(id=ide)
    if request.POST:
        form = EkipakmboForm(request.POST,request.FILES, instance = ekipakmbo)
        if form.is_valid():
            dadus = form.save(commit=False)
            dadus.save()
            messages.success(request,"Dadus Atualiza ho Susessu..!")
            return redirect('listaekipakmbo')
    else:
        formulariu = EkipakmboForm(instance = ekipakmbo)
        context = {
            'form' : formulariu
        }
        return render(request, "ekipakmbo/update.html", context)
@login_required
@allowed_users(allowed_roles=['admin'])
def hamosekipakmbo(request, id):
    ide=decrypt_id(id)
    ekipakmbo = Ekipakmbo.objects.get(id=ide)
    ekipakmbo.delete()
    messages.success(request,"Dadus Apaga  Susessu..!")
    return redirect('listaekipakmbo')

def show(request):
    lingua = request.LANGUAGE_CODE

    if lingua == "en":
        ekipakmbo = Ekipakmbo.objects.filter(lingua__id=3)
    elif lingua == "pt":
        ekipakmbo = Ekipakmbo.objects.filter(lingua__id=2)
    elif lingua == "tet":
        ekipakmbo = Ekipakmbo.objects.filter(lingua__id=1)
    else:
        ekipakmbo = Ekipakmbo.objects.all()  # fallback se lingua la fo

    context = {"ekipakmbo": ekipakmbo}
    return render(request, "ekipakmbo/show.html", context)

