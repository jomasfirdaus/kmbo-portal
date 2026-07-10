from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Foto

def detailufoto(request, galeria_id):
    fotos = Foto.objects.filter(galeria_id=galeria_id)
    return render(request, "foto/detailufoto.html", {'fotos': fotos})



