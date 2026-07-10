from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from main.decorators import allowed_users
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import KategoriaForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import ProtectedError
from main.utils import *

@login_required
@allowed_users(allowed_roles=['admin'])
def listakategoria(request):
    buka = False
    bukatitle = "mamuk"
    
    page_num = request.GET.get('page', 1)

    if request.GET.get('pesquiza'):
        buka = True
        paginator = Paginator(Kategoria.objects.order_by('-id').filter(naran__icontains=request.GET['pesquiza']), 5)
    else:
        paginator = Paginator(Kategoria.objects.order_by('-id'), 5)

    page_range = list(range(1, paginator.num_pages + 1))
    data_Kategoria = paginator.page(page_num)
    page_num_int = int(page_num)

    if buka:
        bukatitle = f"Rezultadu Pesquiza husi <i>' ({request.GET['pesquiza']}) '</i>"

    context = {
        "pajina_imagen": "active",
        "kategoria": data_Kategoria,
        'bukatitle': bukatitle,
        'page_range': page_range,
        'current_page': page_num_int,
    }

    return render(request, "kategoria_notisia/lista.html", context)


@login_required
@allowed_users(allowed_roles=['admin'])
def inputkategoria(request):
    if request.POST:
        forms = KategoriaForm(request.POST, request.FILES)
        if forms.is_valid():
            forms.save()
            messages.success(request, "Dados Rejistu ho Susessu..!")
            return redirect('listakategoria')
    else:
        formulariu = KategoriaForm()

    context = {
        'form': formulariu
    }

    return render(request, "kategoria_notisia/input.html", context)


@login_required
@allowed_users(allowed_roles=['admin'])
def updatekategoria(request, id):
    ide=decrypt_id(id)
    kategoria = get_object_or_404(Kategoria, id=ide)
    if request.POST:
        form = KategoriaForm(request.POST, request.FILES, instance=kategoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Dadus Atualiza ho Susessu..!")
            return redirect('listakategoria')
    else:
        formulariu = KategoriaForm(instance=kategoria)

    context = {
        'form': formulariu
    }

    return render(request, "kategoria_notisia/update.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def hamoskategoria(request, id):
    kategoria = get_object_or_404(Kategoria, id=id)
    try:
        kategoria.delete()
        messages.success(request, "Dadus Apaga Susessu..!")
    except ProtectedError:
        messages.error(request, "La bele apaga tanba Kategoria ne'e uza iha Notisia.")
    return redirect('listakategoria')

