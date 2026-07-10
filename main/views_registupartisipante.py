from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import *
from .forms import RegistuPartisipanteForm
from main.utils import *
from django.db.models import Count


def listaregistupartisipante(request):
    registupartisipante = RegistuPartisipante.objects.all()
    first_three_dezen = registupartisipante.order_by('-id')
    context = {
        "registupartisipante": first_three_dezen
    }
    return render(request, "registupartisipante/lista.html", context)


def inputregistupartisipante(request):
    if request.method == "POST":
        form = RegistuPartisipanteForm(request.POST, request.FILES)
        if form.is_valid():
            dadus = form.save(commit=False)
            dadus.save()
            messages.success(request, "Ita Rejistu ho Susessu!")
            return redirect('listadelgadu')  # troka ba view ne'ebé mostra lista
    else:
        form = RegistuPartisipanteForm()
    
    context = {
        'form': form
    }
    return render(request, "registupartisipante/input.html", context)



def updateregistupartisipante(request, id):
    ide=decrypt_id(id)
    registupartisipante = RegistuPartisipante.objects.get(id=ide)
    if request.method == "POST":
        form = RegistuPartisipanteForm(request.POST, request.FILES, instance=registupartisipante)
        if form.is_valid():
            dadus = form.save(commit=False)
            dadus.save()
            messages.success(request, "Dadus Atualiza ho Susessu!")
            return redirect('listaregistupartisipante')
    else:
        form = RegistuPartisipanteForm(instance=registupartisipante)
    
    context = {
        'form': form
    }
    return render(request, "registupartisipante/update.html", context)


def hamosregistupartisipante(request, id):
    registupartisipante = RegistuPartisipante.objects.get(id=id)
    registupartisipante.delete()
    messages.success(request, "Dadus Apaga Susessu!")
    return redirect('listaregistupartisipante')


def show(request):
    registupartisipante = RegistuPartisipante.objects.all().order_by('-id')
    total = registupartisipante.count()

    def cap_first_letter(s):
        return s.capitalize() if s else s

    def normalize_str(s):
        return s.strip().upper() if s else ''

    # Estatístika Postu
    postu_dict = {}
    for p in registupartisipante:
        key = normalize_str(p.postu)
        if key:
            if key not in postu_dict:
                postu_dict[key] = {'label': cap_first_letter(p.postu), 'count': 0}
            postu_dict[key]['count'] += 1
    postu_labels = [v['label'] for v in postu_dict.values()]
    postu_data = [v['count'] for v in postu_dict.values()]
    postu_percent = [round((c / total) * 100, 2) if total else 0 for c in postu_data]

    # Estatístika Kategoria
    kategoria_dict = {}
    for p in registupartisipante:
        key = normalize_str(p.kategoria)
        if key:
            if key not in kategoria_dict:
                kategoria_dict[key] = {'label': cap_first_letter(p.kategoria), 'count': 0}
            kategoria_dict[key]['count'] += 1
    kategoria_labels = [v['label'] for v in kategoria_dict.values()]
    kategoria_data = [v['count'] for v in kategoria_dict.values()]
    kategoria_percent = [round((c / total) * 100, 2) if total else 0 for c in kategoria_data]

    # Estatístika Sexo
    sexo_dict = {}
    for p in registupartisipante:
        s_norm = normalize_str(p.sexo)
        if s_norm not in sexo_dict:
            if s_norm == 'M':
                label = 'Mane'
            elif s_norm == 'F':
                label = 'Feto'
            else:
                label = p.sexo or 'La hatene'
            sexo_dict[s_norm] = {'label': label, 'count': 0}
        sexo_dict[s_norm]['count'] += 1
    sexo_labels = [v['label'] for v in sexo_dict.values()]
    sexo_data = [v['count'] for v in sexo_dict.values()]
    sexo_percent = [round((c / total) * 100, 2) if total else 0 for c in sexo_data]

   

    context = {
        "registupartisipante": registupartisipante,
        "postu_labels": postu_labels,
        "postu_data": postu_data,
        "postu_percent": postu_percent,
        "kategoria_labels": kategoria_labels,
        "kategoria_data": kategoria_data,
        "kategoria_percent": kategoria_percent,
        "sexo_labels": sexo_labels,
        "sexo_data": sexo_data,
        "sexo_percent": sexo_percent,
        
    }

    return render(request, "registupartisipante/show.html", context)
