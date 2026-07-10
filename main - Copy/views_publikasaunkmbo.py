from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import *
from .forms import PublikasaunkmboForm
from main.utils import *
from main.decorators import allowed_users
from PIL import Image, ImageOps

import qrcode
from django.http import HttpResponse
from io import BytesIO



@login_required
@allowed_users(allowed_roles=['admin'])
def listapublikasaunkmbo(request):
    publikasaunkmbo = Publikasaunkmbo.objects.all().order_by('-id')
    
    qr_dict = {}
    for item in publikasaunkmbo:
        file_url = request.build_absolute_uri(item.file_pdf.url)
        qr_code_b64 = generate_qr_code_base64(file_url)
        qr_dict[item.id] = qr_code_b64
    
    context = {
        "publikasaunkmbo": publikasaunkmbo,
        "qr_dict": qr_dict,
    }
    return render(request, "publikasaunkmbo/lista.html", context)



@login_required
@allowed_users(allowed_roles=['admin'])
def inputpublikasaunkmbo(request):
    if request.method == "POST":
        form = PublikasaunkmboForm(request.POST, request.FILES)
        if form.is_valid():
            dadus = form.save(commit=False)
            dadus.save()
            messages.success(request, "Dados Rejistu ho Susessu!")
            return redirect('listapublikasaunkmbo')
    else:
        form = PublikasaunkmboForm()
    
    context = {
        'form': form
    }
    return render(request, "publikasaunkmbo/input.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def updatepublikasaunkmbo(request, id):
    ide=decrypt_id(id)
    publikasaunkmbo = Publikasaunkmbo.objects.get(id=ide)
    if request.method == "POST":
        form = PublikasaunkmboForm(request.POST, request.FILES, instance=publikasaunkmbo)
        if form.is_valid():
            dadus = form.save(commit=False)
            dadus.save()
            messages.success(request, "Dadus Atualiza ho Susessu!")
            return redirect('listapublikasaunkmbo')
    else:
        form = PublikasaunkmboForm(instance=publikasaunkmbo)
    
    context = {
        'form': form
    }
    return render(request, "publikasaunkmbo/update.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def hamospublikasaunkmbo(request, id):
    publikasaunkmbo = Publikasaunkmbo.objects.get(id=id)
    publikasaunkmbo.delete()
    messages.success(request, "Dadus Apaga Susessu!")
    return redirect('listapublikasaunkmbo')

def show(request):
    publikasaunkmbo = Publikasaunkmbo.objects.all()
    first_three_dezen = publikasaunkmbo.order_by('-id')
    
    lingua = request.LANGUAGE_CODE
    if lingua == "en":
        first_three_dezen = publikasaunkmbo.filter(lingua__id=3).order_by('-id')
    elif lingua == "pt":
        first_three_dezen = publikasaunkmbo.filter(lingua__id=2).order_by('-id')
    elif lingua == "pt-br":
        first_three_dezen = publikasaunkmbo.filter(lingua__id=1).order_by('-id')
   
    context = {
        "publikasaunkmbo": first_three_dezen
    }
    return render(request, "publikasaunkmbo/show.html", context)


@login_required
@allowed_users(allowed_roles=['admin'])
def download_qr_code(request, id):
    ide = decrypt_id(id)
    publikasaun = Publikasaunkmbo.objects.get(id=ide)
    file_url = request.build_absolute_uri(publikasaun.file_pdf.url)

    # Halo QR
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=2,
        border=2
    )
    qr.add_data(file_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white').convert("RGB")  # Convert ba RGB

    # Muda border color ho PIL (ex: muda ba light gray)
    border_color = (255, 0, 0)  # red (RGB)

    border_size = 5  # px

    # Adiciona border color personalizado
    img_with_border = ImageOps.expand(img, border=border_size, fill=border_color)

    buffer = BytesIO()
    img_with_border.save(buffer, format="PNG")
    buffer.seek(0)

    response = HttpResponse(buffer, content_type="image/png")
    response['Content-Disposition'] = f'attachment; filename=qr_publikasaun_{ide}.png'
    return response



