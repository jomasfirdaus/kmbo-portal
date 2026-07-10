from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main.decorators import allowed_users
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import *
from datetime import datetime
from .forms import AnunsiuForm
from django.contrib import messages
# from main.forms import SingleauditForm
from main.utils import *


@login_required
@allowed_users(allowed_roles=['admin'])
def listaanunsiu(request):
    buka = False
    bukatitle = "mamuk"
    if request.GET.__contains__('page') :
        page_num = request.GET.get('page')
    else:
        page_num = 1
    if request.GET.__contains__('pesquiza'):
        buka = True
        paginator = Paginator(Anunsiu.objects.order_by('-id').filter(naran__icontains=request.GET['pesquiza']), 1)
    else:
        paginator = Paginator(Anunsiu.objects.order_by('-id'), 5)

    page_range = []
    for i in range(paginator.num_pages):
        page_range.append(i+1)
        data_Anunsiu = paginator.page(page_num)
        page_num_int = int(page_num)

    if buka :
        bukatitle = "Rezultadu Pesquiza husi <i>' (" + request.GET['pesquiza'] + ") '</i>"
   
    context = {
        "pajina_imagen" : "active",
        "anunsiu" : data_Anunsiu,
        'bukatitle' : bukatitle,
        'page_range' : page_range,
        'current_page' : page_num_int,
        }
   
    return render(request, "anunsiu/lista.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def inputanunsiu(request):
    if request.method == 'POST':
        forms = AnunsiuForm(request.POST, request.FILES)
        if forms.is_valid():
            dadus = forms.save(commit=False)
            dadus.save()
            files = request.FILES.getlist('dokumentu')

            for f in files:
                file_instance = Dokumentu.objects.create(file=f)
                dadus.dokumentu.add(file_instance)
            dadus.save()
            messages.success(request, "Imajen Rejistu ho Susessu..!")
            return redirect('listaanunsiu')
    else:
        formulariu = AnunsiuForm()
    context = {
        'form': formulariu
        }
    return render(request, 'anunsiu/input.html', context)

@login_required
@allowed_users(allowed_roles=['admin'])
def updateanunsiu(request, id):
    ide=decrypt_id(id)
    anunsiu = Anunsiu.objects.get(id=ide)
    if request.POST:
        form = AnunsiuForm(request.POST,request.FILES, instance = anunsiu)
        if form.is_valid():
            dadus = form.save(commit=False)
            dadus.save()
            messages.success(request,"Dadus Atualiza ho Susessu..!")
            return redirect('listaanunsiu')
    else:
        formulariu = AnunsiuForm(instance = anunsiu)
        context = {
            'form' : formulariu
        }
        return render(request, "anunsiu/update.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def hamosanunsiu(request, id):
    ide=decrypt_id(id)
    anunsiu = Anunsiu.objects.get(id=ide)
    anunsiu.delete()
    messages.success(request,"Dadus Apaga  Susessu..!")
    return redirect('listaanunsiu')

def showanunsiu(request):
    # Foti data ohin loron
    today = datetime.now()

    # Filtra anunsiu tuir data remata (anunsiu ne'ebe seidauk remata)
    anunsiu = Anunsiu.objects.filter(dataremata__gte=today).order_by('-datapublikasuan')

    lingua = request.LANGUAGE_CODE

    # Filtra tuir lingua
    if lingua == "en":
        anunsiu = anunsiu.filter(lingua__id=3)
    elif lingua == "pt":
        anunsiu = anunsiu.filter(lingua__id=2)
    elif lingua == "pt-br":
        anunsiu = anunsiu.filter(lingua__id=1)

    context = {
        "anunsiu": anunsiu
    }
    return render(request, "anunsiu/show.html", context)
