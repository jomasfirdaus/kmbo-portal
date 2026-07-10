from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main.decorators import allowed_users
from django.views.decorators.csrf import csrf_exempt
from .models import Galeria, Foto
from .forms import GaleriaForm
from django.contrib import messages
from django.db.models import ProtectedError
from main.utils import *
from django.db.models.functions import ExtractYear
from django.db.models import Count


@login_required
@allowed_users(allowed_roles=['admin'])
def galeria(request):
    galeria = Galeria.objects.all()
    first_three_galeria = galeria.order_by('-id')
    context = {
        "galeria": first_three_galeria
    }
    return render(request, "galeria/lista.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def inputgaleria(request):
    if request.method == 'POST':
        forms = GaleriaForm(request.POST, request.FILES)
        if forms.is_valid():
            dadus = forms.save(commit=False)
            dadus.save()
            messages.success(request, "Dados Rejistu ho Susessu..!")
            return redirect('galeria')
    else:
        forms = GaleriaForm()  # Corrigido para manter a mesma variável "forms"

    # Atribui context após o if-else
    context = {
        'form': forms
    }

    return render(request, "galeria/kria.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def updategaleria(request, id):
    ide=decrypt_id(id)
    galeria = Galeria.objects.get(id=ide)
    if request.POST:
        form = GaleriaForm(request.POST, request.FILES, instance=galeria)
        if form.is_valid():
            dadus = form.save(commit=False)
            dadus.save()
            messages.success(request, "Dadus Atualiza ho Susessu..!")
            return redirect('galeria')
    else:
        form = GaleriaForm(instance=galeria)
        context = {
            'form': form
        }
        return render(request, "galeria/update.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def hamosgaleria(request, id):
    try:
        galeria = Galeria.objects.get(id=id)
        foto_objects = Foto.objects.filter(galeria=galeria)
        foto_objects.update(galeria=None)
        galeria.delete()
        messages.success(request, "Dadus Apaga Susessu..!")
        return redirect('galeria')
    except ProtectedError:
        messages.error(request, "Cannot delete because of protected foreign key references.")
        return redirect('galeria')



def showcover(request):
    galeria = Galeria.objects.all()
    lingua = request.LANGUAGE_CODE

    if lingua == "en":
        galeria = galeria.filter(lingua__id=3).order_by('-id')
    elif lingua == "pt":
        galeria = galeria.filter(lingua__id=2).order_by('-id')
    elif lingua == "tet":
        galeria = galeria.filter(lingua__id=1).order_by('-id')
    else:
        galeria = galeria.order_by('-id')

    # Tau lista tinan hodi fó dinamiku filter iha frontend
    tinan_qs = galeria.annotate(year=ExtractYear('data')).values('year').annotate(count=Count('id')).order_by('-year')
    tinan_list = [item['year'] for item in tinan_qs]

    context = {
        "galeria": galeria,
        "tinan_list": tinan_list,
    }
    return render(request, "galeria/showcover.html", context)


def show(request):
    return render(request, "galeria/show.html")
