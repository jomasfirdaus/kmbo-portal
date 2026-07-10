from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import ParseiruSiraForm
from django.contrib import messages
from main.utils import *
from main.decorators import allowed_users

@login_required
@allowed_users(allowed_roles=['admin'])
def listaparseirusira(request):
    parseirusira = ParseiruSira.objects.all()
    first_parseiru = parseirusira.order_by('-id')
    context = {
        "parseirusira" : first_parseiru
        }
    return render(request, "parseirusira/lista.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def inputparseirusira(request):
    if request.method == 'POST':
        forms = ParseiruSiraForm(request.POST, request.FILES)
        if forms.is_valid():
            dadus = forms.save(commit=False)
            dadus.save()
            messages.success(request, "Dados Rejistu ho Susessu..!")
            return redirect('listaparseirusira')
        else:
            # Form invalid – show form with errors
            context = {'form': forms}
    else:
        formulariu = ParseiruSiraForm()
        context = {'form': formulariu}
        
    return render(request, "parseirusira/input.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def updateparseirusira(request, id):
    ide = decrypt_id(id)
    parseirusira = ParseiruSira.objects.get(id=ide)
    
    if request.method == "POST":
        form = ParseiruSiraForm(request.POST, request.FILES, instance=parseirusira)
        if form.is_valid():
            dadus = form.save(commit=False)
            dadus.save()
            messages.success(request, "Dadus Atualiza ho Susessu..!")
            return redirect('listaparseirusira')
        # ⬇️ render form with validation errors
        context = {'form': form}
        return render(request, "parseirusira/update.html", context)
    else:
        formulariu = ParseiruSiraForm(instance=parseirusira)
        context = {'form': formulariu}
        return render(request, "parseirusira/update.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def hamosparseirusira(request, id):
    ide=decrypt_id(id)
    parseirusira = ParseiruSira.objects.get(id=ide)
    parseirusira.delete()
    messages.success(request,"Dadus Apaga  Susessu..!")
    return redirect('listaparseirusira')

def show(request):
     parseirusira = ParseiruSira.objects.all()
     return render(request, "parseirusira/show.html")