from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main.decorators import allowed_users
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import InfojeralkmboForm
from django.contrib import messages
from main.utils import *

@login_required
@allowed_users(allowed_roles=['admin'])
def listainfojeralkmbo(request):
    infojeralkmbo = Infojeralkmbo.objects.all()
    first_infojeralkmbo = infojeralkmbo.order_by('-id')
    context = {
        "infojeralkmbo" : first_infojeralkmbo
        }
    return render(request, "infojeralkmbo/lista.html", context)
@login_required
@allowed_users(allowed_roles=['admin'])
def inputinfojeralkmbo(request):
   if request.method=='POST':
        forms = InfojeralkmboForm(request.POST,request.FILES)
        if forms.is_valid():
            dadus = forms.save(commit=False)
            dadus.save()
            messages.success(request,"Dados Rejistu  ho Susessu..!")
            return redirect('listainfojeralkmbo')
   else:
        formulariu = InfojeralkmboForm()
        context ={
            
            'form': formulariu}
   return render(request, "infojeralkmbo/input.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])#infojeralkmbo
def updateinfojeralkmbo(request, id):
    ide=decrypt_id(id)
    infojeralkmbo = Infojeralkmbo.objects.get(id=ide)
    if request.POST:
        form = InfojeralkmboForm(request.POST,request.FILES, instance = infojeralkmbo)
        if form.is_valid():
            dadus = form.save(commit=False)
            dadus.save()
            messages.success(request,"Dadus Atualiza ho Susessu..!")
            return redirect('listainfojeralkmbo')
    else:
        formulariu = InfojeralkmboForm(instance = infojeralkmbo)
        context = {
            'form' : formulariu
        }
        return render(request, "infojeralkmbo/update.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def hamosinfojeralkmbo(request, id):
    ide=decrypt_id(id)
    infojeralkmbo = Infojeralkmbo.objects.get(id=ide)
    infojeralkmbo.delete()
    messages.success(request,"Dadus Apaga  Susessu..!")
    return redirect('listainfojeralkmbo')

def show(request):
     infojeralkmbo = Infojeralkmbo.objects.all()
     return render(request, "infojeralkmbo/show.html")