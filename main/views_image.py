from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from main.decorators import allowed_users
from django.views.decorators.csrf import csrf_exempt
from .models import Imajen
from .forms import ImajenForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import ProtectedError
from main.utils import *

@login_required
@allowed_users(allowed_roles=['admin'])
def imajen(request):
    buka = False
    bukatitle = "mamuk"

    # Pagination
    page_num = request.GET.get('page', 1)  # Default to page 1
    search_query = request.GET.get('pesquiza', None)

    if search_query:
        buka = True
        imajen_list = Imajen.objects.filter(naran__icontains=search_query).order_by('-id')
        bukatitle = f"Rezultadu Pesquiza husi <i>' ({search_query}) '</i>"
    else:
        imajen_list = Imajen.objects.all().order_by('-id')

    paginator = Paginator(imajen_list, 5)  # Show 5 images per page
    data_Imagen = paginator.get_page(page_num)  # Fetch the current page data
    page_range = paginator.page_range  # Get the range of pages

    context = {
        "pajina_imagen": "active",
        "imajen": data_Imagen,
        'bukatitle': bukatitle,
        'page_range': page_range,
        'current_page': int(page_num),
    }

    return render(request, "imajen/lista.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def inputimajen(request):
    if request.method == 'POST':
        forms = ImajenForm(request.POST, request.FILES)
        if forms.is_valid():
            forms.save()
            messages.success(request, "Dados Rejistu ho Susessu..!")
            return redirect('imajen')
    else:
        forms = ImajenForm()

    context = {
        'form': forms
    }
    
    return render(request, "imajen/input.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def update(request, id):
    ide=decrypt_id(id)
    imajen = get_object_or_404(Imajen, id=ide)  # Use get_object_or_404 for better error handling
    if request.method == 'POST':
        form = ImajenForm(request.POST, request.FILES, instance=imajen)
        if form.is_valid():
            form.save()
            messages.success(request, "Dadus Atualiza ho Susessu..!")
            return redirect('imajen')
    else:
        form = ImajenForm(instance=imajen)

    context = {
        'form': form
    }
    
    return render(request, "imajen/update.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def hamos(request, id):
    try:
        imajen = get_object_or_404(Imajen, id=id)
        imajen.delete()
        messages.success(request, "Dadus Apaga ho Susessu!")
    except ProtectedError:
        messages.error(request, "La bele apaga tanba imajen ne'e uza iha Notisia.")
    return redirect('imajen')
