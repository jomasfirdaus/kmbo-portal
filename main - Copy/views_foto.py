from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main.decorators import allowed_users
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import FotoForm
from django.contrib import messages
from .models import Foto, Galeria
from django.shortcuts import render, get_object_or_404
from main.utils import *

@login_required
@allowed_users(allowed_roles=['admin'])
def foto(request, galeria_id):
    galeria = get_object_or_404(Galeria, pk=galeria_id)
    foto = Foto.objects.filter(galeria=galeria)
    first_foto = foto.order_by('-id')
    galeria = Galeria.objects.get(id=galeria_id)
   
    context = {
        "foto" : first_foto,
        "id": galeria_id,
        "galeria":galeria.titulu
        
        }
   
    return render(request, "foto/lista.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def inputfoto(request, galeria_id):
    if request.method == 'POST':
        form = FotoForm(request.POST, request.FILES)
        if form.is_valid():
            # Salva a galeria
            dadus = form.save(commit=False)
            dadus.save()

            # Processa arquivos
            files = request.FILES.getlist('foto')
            for f in files:
                file_instance = Pic.objects.create(pic=f)  # Salva a imagem
                dadus.foto.add(file_instance)  # Adiciona a imagem à relação
            dadus.save()
            messages.success(request, "Imajen Rejistu ho Susessu..!")
            return redirect('foto', galeria_id=galeria_id)
    else:
        formulariu = FotoForm()
    context = {
        'foto': formulariu
    }
    return render(request, 'foto/kria.html', context)

@login_required
@allowed_users(allowed_roles=['admin'])
def updatefoto(request, id):
    ide=decrypt_id(id)
    foto = get_object_or_404(Foto, id=ide)
    if request.POST:
        form = FotoForm(request.POST,request.FILES, instance = foto)
        if form.is_valid():
            dadus = form.save(commit=False)
            dadus.save()
            messages.success(request,"Dadus Atualiza ho Susessu..!")
            return redirect('foto',galeria_id=dadus.galeria_id)
    else:
        formulariu = FotoForm(instance = foto)
        context = {
            'foto' : formulariu
        }
        return render(request, "foto/update.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def hamosfoto(request, id):
    foto = get_object_or_404(Foto, id=id)
    foto.delete()
    messages.success(request,"Dadus Apaga  Susessu..!")
    return redirect('foto', galeria_id = foto.galeria_id)

@login_required
@allowed_users(allowed_roles=['admin'])
def detailufoto(request, galeria_id):
    galeria = get_object_or_404(Galeria, pk=galeria_id)
    foto = Foto.objects.filter(galeria=galeria)

    context = {
        "foto": foto,
        "id": galeria_id,
        "galeria": galeria  # hatama object, la'os galeria.titulu
    }

    return render(request, "foto/detailufoto.html", context)



