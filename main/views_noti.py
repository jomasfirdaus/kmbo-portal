from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import NotisiaForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from main.utils import *
from django.db.models import Count
from main.decorators import allowed_users


@login_required
@allowed_users(allowed_roles=['admin'])
def listanoti(request):
    buka = False
    bukatitle = "mamuk"
    
    # Obter o número da página
    page_num = request.GET.get('page', 1)

    # Verifica se há uma pesquisa
    if 'pesquiza' in request.GET:
        buka = True
        query = request.GET['pesquiza']
        notisias_queryset = Notisia.objects.filter(naran__icontains=query).order_by('-id')
        paginator = Paginator(notisias_queryset, 1)  # Um item por página para pesquisa
    else:
        notisias_queryset = Notisia.objects.all().order_by('-id')
        paginator = Paginator(notisias_queryset, 5)  # 5 itens por página

    # Obter a página correspondente
    try:
        data_Imagen = paginator.page(page_num)
    except (EmptyPage, PageNotAnInteger):
        data_Imagen = paginator.page(1)  # Se a página não existir, retorna a primeira

    page_range = range(1, paginator.num_pages + 1)  # Cria uma faixa de páginas

    if buka:
        bukatitle = f"Rezultadu Pesquiza husi <i>' ({query}) '</i>"
    
    # Contexto a ser passado para o template
    context = {
        "pajina_imagen": "active",
        "noti": data_Imagen,
        'bukatitle': bukatitle,
        'page_range': page_range,
        'current_page': int(page_num),
    }
    
    # Retorna a resposta renderizada
    return render(request, "noti/lista.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def inputnoti(request):
    if request.POST:
        forms = NotisiaForm(request.POST,request.FILES)
        if forms.is_valid():
            dadus = forms.save(commit=False)
            dadus.status = 'Pendente'
            dadus.save()
            messages.success(request,"Dados Rejistu  ho Susessu..!")
            return redirect('listanoti')
    else:
        formulariu = NotisiaForm()
        context ={
            
            'form': formulariu}

    return render(request, "noti/input.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def updatenoti(request, id):
    ide=decrypt_id(id)
    noti = Notisia.objects.get(id=ide)
    if request.method == 'POST':
        form = NotisiaForm(request.POST, request.FILES, instance=noti)
        if form.is_valid():
            form.save()
            messages.success(request, "Dadus Atualiza ho Susessu..!")
            return redirect('listanoti')
    else:
        form = NotisiaForm(instance=noti)
    
    context = {
        'form': form
    }
    return render(request, "noti/update.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def hamosnoti(request, id):
    noti = Notisia.objects.get(id=id)
    noti.delete()
    messages.success(request,"Dadus Apaga  Susessu..!")
    return redirect('listanoti')

def detailnotisia(request, id):
    id=decrypt_id(id)
    print(id)
    noti = Notisia.objects.get(id=id)
    context={
        'noti':noti
    }
    return render(request, "noti/detailnotisia.html", context) 

def editor(request, id):
    ide=decrypt_id(id)
    noti = Notisia.objects.get(id=ide)
    if request.method == 'POST':
        form = NotisiaForm(request.POST, request.FILES, instance=noti)
        if form.is_valid():
            form.save()
            messages.success(request, "Dadus Atualiza ho Susessu..!")
            return redirect('detallu', id=id)
    else:
        form = NotisiaForm(instance=noti)
    
    context = {
        'atualiza': form
    }
    return render(request, "noti/editor.html", context)

    
def notisia(request):
    notisia = Notisia.objects.all()
    context = {
        "notisia" : notisia,
        }
    return render(request, "noti/lista.html", context)

def reviewona(request, id):
    id=decrypt_id(id)
    Notisia.objects.filter(id=id).update(status="Review")
    return redirect('detallu' , encrypt_id(id))

def publika(request, id):
    id=decrypt_id(id)
    Notisia.objects.filter(id=id).update(status="Publika")
    return redirect('detallu' , encrypt_id(id))

def kansela(request, id):
    id=decrypt_id(id)
    Notisia.objects.filter(id=id).update(status="Pendente")
    return redirect('detallu' , encrypt_id(id))



def shownotisia1(request):
    lingua = request.LANGUAGE_CODE
    notisia = Notisia.objects.filter(status="Publika")

    if lingua == "tet":
        notisia = notisia.filter(lingua__id=1)
    elif lingua == "pt":
        notisia = notisia.filter(lingua__id=2)
    elif lingua == "en":
        notisia = notisia.filter(lingua__id=3)

    # Filtra kategoria se iha query
    kategoria_slug = request.GET.get("kategoria")
    if kategoria_slug:
        notisia = notisia.filter(kategoria__slug=kategoria_slug)

    # Notisia foun sira (3 liu ba header/featured)
    first_notisia1 = notisia.order_by('-datapublika')

    # Pagination
    paginator = Paginator(first_notisia1, 5)  # 5 notisia/1 página
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Notisia relevante (seluk)
    notisiaseluk = notisia.order_by('-datapublika')[:5]

    # Kategoria ho total
    kategorias = Kategoria.objects.annotate(total=Count('notisia'))

    context = {
        "notisiaseluk": notisiaseluk,
        "notisia": page_obj,  # Agora iha pagination
        "kategorias": kategorias,
        "is_paginated": page_obj.has_other_pages(),
        "page_obj": page_obj,
    }
    return render(request, "noti/show1.html", context)


def shownotisia(request, slug):
    from django.db.models import Count
    
    lingua = request.LANGUAGE_CODE
    notisia = Notisia.objects.get(slug=slug)
    
    # Filter related news by language
    notisiaseluk = Notisia.objects.filter(status="Publika")
    
    if lingua == "tet":
        notisiaseluk = notisiaseluk.filter(lingua__id=1)
    elif lingua == "pt":
        notisiaseluk = notisiaseluk.filter(lingua__id=2)
    elif lingua == "en":
        notisiaseluk = notisiaseluk.filter(lingua__id=3)
    
    # Exclude the current news article from related news
    notisiaseluk = notisiaseluk.exclude(slug=slug).order_by('-datapublika')[:5]
    
    # Get categories with count (optional)
    kategorias = Kategoria.objects.annotate(total=Count('notisia'))
    
    context = {
        "notisiaseluk": notisiaseluk,
        "notisia": notisia,
        "kategorias": kategorias,  # Optional: if you want to show categories in template
    }
    return render(request, "noti/show.html", context)