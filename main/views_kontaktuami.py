from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main.decorators import allowed_users
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import KontaktuamiForm
from django.contrib import messages
from main.utils import * 

@login_required
@allowed_users(allowed_roles=['admin'])
def listakontaktuami(request):
    kontaktuami = Kontaktuami.objects.all()
    first_mensajenhusikordenador = kontaktuami.order_by('-id')
    context = {
        "kontaktuami" : first_mensajenhusikordenador
        }
    return render(request, "kontaktuami/lista.html", context)




def updatekontaktuami(request, id):
    ide=decrypt_id(id)
    kontaktuami = Kontaktuami.objects.get(id=ide)
    if request.POST:
        form = KontaktuamiForm(request.POST,request.FILES, instance = kontaktuami)
        if form.is_valid():
            dadus = form.save(commit=False)
            dadus.save()
            messages.success(request,"Dadus Atualiza ho Susessu..!")
            return redirect('listakontaktuami')
    else:
        formulariu = KontaktuamiForm(instance = kontaktuami)
        context = {
            'form' : formulariu
        }
        return render(request, "kontaktuami/update.html", context)


def show(request):
     kontaktuami = Kontaktuami.objects.all()
     return render(request, "kontaktuami/show.html")