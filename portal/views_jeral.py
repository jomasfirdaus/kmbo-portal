from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as loginadmin
from django.contrib.auth.models import User, auth
from .forms import User
from main.models import *
from portal.models import *
from .models import Rejistu
from django.contrib.auth.decorators import login_required

from django.db.models import Count

def home(request):
    kontaktuami = Kontaktuami.objects.first()
    context = {
        "kontaktuami": kontaktuami,
    }
    return render(request, 'portal/kmbomenu.html', context)


def dashboardkmbo(request):
    lingua = request.LANGUAGE_CODE
    LINGUA_IDS = {
        "tet": 1,
        "pt": 2,
        "en": 3
    }
    lingua_id = LINGUA_IDS.get(lingua)

    # Filtra status "Publika" ba notísia hotu dashboardtic
    noti_info = Notisia.objects.filter(kategoria__naran='Informasaun', status='Publika') 
    noti_news = Notisia.objects.filter(kategoria__naran='Notisia', status='Publika') 
    noti_papel = Notisia.objects.filter(kategoria__naran='Papel', status='Publika')
    noti = noti_info | noti_news | noti_papel

    # Filtra ho lingua
    if lingua_id:
        first_three_noti2 = noti.filter(lingua__id=lingua_id).order_by('-datapublika')[:15]
    else:
        first_three_noti2 = noti.order_by('-datapublika')[:10]

    # Filtra notisia hotu ho status "Publika"
    notisia = Notisia.objects.filter(status='Publika')
    if lingua_id:
        first_three_noti = notisia.filter(lingua__id=lingua_id).order_by('-datapublika')[:5]
    else:
        first_three_noti = notisia.order_by('-datapublika')[:5]

    # Parseiru, mensajen husi koordenador, etc. (mantém)
    if lingua_id:
        parseirusira = ParseiruSira.objects.filter(lingua__id=lingua_id)
        mensajenhusikordenador = Mensajenhusikordenador.objects.filter(lingua__id=lingua_id).order_by('-id')
        infojeralkmbo = Infojeralkmbo.objects.filter(lingua_id=lingua_id).order_by('-id')
        atividade = Atividade.objects.filter(lingua_id=lingua_id).order_by('-id')
    else:
        parseirusira = ParseiruSira.objects.all()
        mensajenhusikordenador = Mensajenhusikordenador.objects.all().order_by('-id')
        infojeralkmbo = Infojeralkmbo.objects.all().order_by('-id')
        atividade = Atividade.objects.all().order_by('-id')
    context = {
        "noti": first_three_noti2,
        "first_three_noti": first_three_noti,
        "parseirusira": parseirusira,
        "mensajenhusikordenador": mensajenhusikordenador,
        "infojeralkmbo": infojeralkmbo,
        "atividade": atividade,  # Hatama ne'e
    }

    return render(request, 'portal/sidebarkmbo.html', context)

def master(request):
    return render (request, 'portal/sidebarkmbo.html')

@login_required
def main(request):    
    user_profile = Rejistu.objects.get(user=request.user)

    context = {
        'main': user_profile
    } 
    return render(request, "portal/main.html", context)

def logout(request):
    auth.logout(request)
    return redirect( "login")

def dashboard(request):
    contact_count = Kontaktu.objects.count()
    status_counts = Notisia.objects.values('status').annotate(status_count=Count('status'))

    counts_dict = {
        'pendente_count': 0,
        'review_count': 0,
        'publika_count': 0,
        'contact_count': contact_count
    }

    for status_count in status_counts:
        status = status_count['status']
        if status == 'Pendente':
            counts_dict['pendente_count'] = status_count['status_count']
        elif status == 'Review':
            counts_dict['review_count'] = status_count['status_count']
        elif status == 'Publika':
            counts_dict['publika_count'] = status_count['status_count']
    
    return render(request, "portal/dashboard.html",counts_dict )