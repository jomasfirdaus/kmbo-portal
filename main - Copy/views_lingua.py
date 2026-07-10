from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main.decorators import allowed_users
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import LinguaForm
from django.contrib import messages

@login_required
@allowed_users(allowed_roles=['admin'])
def lingua(request):
  
    lingua = Lingua.objects.all().order_by('-id')
   
    context = {
        "lingua" : lingua,
        }
    
    return render(request, "lingua/index.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def inputlingua(request):
    if request.POST:
        forms = LinguaForm(request.POST,request.FILES)
        if forms.is_valid():
            dadus = forms.save(commit=False)
            dadus.save()
            messages.success(request,"Dados Rejistu  ho Susessu..!")
            return redirect('lingua')
    else:
        formulariu = LinguaForm()
        context ={
            
            'form': formulariu}

    return render(request, "lingua/input.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def update(request, id):
    lingua = Lingua.objects.get(id=id)
    if request.POST:
        form = LinguaForm(request.POST,request.FILES, instance = lingua)
        if form.is_valid():
            dadus = form.save(commit=False)
            dadus.save()
            messages.success(request,"Dadus Atualiza ho Susessu..!")
            return redirect('lingua')
    else:
        formulariu = LinguaForm(instance = lingua)
        context = {
            'form' : formulariu
        }
        return render(request, "lingua/update.html", context)


@login_required
@allowed_users(allowed_roles=['admin'])
def hamos(request, id):
    lingua = Lingua.objects.get(id=id)
    lingua.delete()
    messages.success(request,"Dadus hamos  Susessu..!")
    return redirect('lingua')





