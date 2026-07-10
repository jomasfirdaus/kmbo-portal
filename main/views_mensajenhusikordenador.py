from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main.decorators import allowed_users

from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import MensajenhusikordenadorForm
from django.contrib import messages
from main.utils import *


@login_required
@allowed_users(allowed_roles=['admin'])
def listamensajenhusikordenador(request):
    mensajenhusikordenador = Mensajenhusikordenador.objects.all()
    first_mensajenhusikordenador = mensajenhusikordenador.order_by('-id')
    context = {
        "mensajenhusikordenador" : first_mensajenhusikordenador
        }
    return render(request, "mensajenhusikordenador/lista.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def inputmensajenhusikordenador(request):
   if request.method=='POST':
        forms = MensajenhusikordenadorForm(request.POST,request.FILES)
        if forms.is_valid():
            dadus = forms.save(commit=False)
            dadus.save()
            messages.success(request,"Dados Rejistu  ho Susessu..!")
            return redirect('listamensajenhusikordenador')
   else:
        formulariu = MensajenhusikordenadorForm()
        context ={
            
            'form': formulariu}
   return render(request, "mensajenhusikordenador/input.html", context)


@login_required
@allowed_users(allowed_roles=['admin'])#mensajenhusikordenador
def updatemensajenhusikordenador(request, id):
    ide=decrypt_id(id)
    mensajenhusikordenador = Mensajenhusikordenador.objects.get(id=ide)
    if request.POST:
        form = MensajenhusikordenadorForm(request.POST,request.FILES, instance = mensajenhusikordenador)
        if form.is_valid():
            dadus = form.save(commit=False)
            dadus.save()
            messages.success(request,"Dadus Atualiza ho Susessu..!")
            return redirect('listamensajenhusikordenador')
    else:
        formulariu = MensajenhusikordenadorForm(instance = mensajenhusikordenador)
        context = {
            'form' : formulariu
        }
        return render(request, "mensajenhusikordenador/update.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def hamosmensajenhusikordenador(request, id):
    ide=decrypt_id(id)
    mensajenhusikordenador = Mensajenhusikordenador.objects.get(id=ide)
    mensajenhusikordenador.delete()
    messages.success(request,"Dadus Apaga  Susessu..!")
    return redirect('listamensajenhusikordenador')

def show(request):
     mensajenhusikordenador = Mensajenhusikordenador.objects.all()
     return render(request, "mensajenhusikordenador/show.html")