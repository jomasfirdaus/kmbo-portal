from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main.decorators import allowed_users
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import KontaktuForm
from django.contrib import messages

@login_required
@allowed_users(allowed_roles=['admin'])
def listakontaktu(request):
    kontaktu = Kontaktu.objects.all()
    first_kontak = kontaktu.order_by('-id')
    context = {
        "kontaktu" : first_kontak
        }
    
    return render(request, "kontaktu/lista.html", context)


def inputokontaktu(request):
    kontaktuami = Kontaktuami.objects.first()  # Tau `first()` ho segurança atu evita empty queryset error
    if request.method == 'POST':
        forms = KontaktuForm(request.POST, request.FILES)
        if forms.is_valid():
            forms.save()
            messages.success(request, "Ita nia Mensajen Haruka ho susesu, Hein resposta husi KMBO!")
            return redirect('inputokontaktu')
    else:
        forms = KontaktuForm()

    context = {
        'kontaktuami': kontaktuami,
        'form': forms,
    }
    return render(request, "kontaktu/input.html", context)


@login_required
@allowed_users(allowed_roles=['admin'])
def hamoskontaktu(request, id):
    kontaktu = Kontaktu.objects.get(id=id)
    kontaktu.delete()
    messages.success(request,"Dadus Apaga  Susessu..!")
    return redirect('listakontaktu')

