from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import VideoForm
from django.contrib import messages
from django.db.models.functions import ExtractYear
from main.decorators import allowed_users

@login_required
@allowed_users(allowed_roles=['admin'])
def video(request):   
    video = Video.objects.all()
    first_three_video = video.order_by('-id')[:3]
    context = {
        "video" : first_three_video
        }
    return render(request, "video/lista.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def inputvideo(request):
   if request.method=='POST':
        forms = VideoForm(request.POST,request.FILES)
        if forms.is_valid():
            dadus = forms.save(commit=False)
            dadus.save()
            messages.success(request,"Dados Rejistu  ho Susessu..!")
            return redirect('video')
   else:
        formulariu = VideoForm()
        context ={
            
            'form': formulariu}

   return render(request, "video/kria.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def updatevideo(request, id):
    video = Video.objects.get(id=id)
    if request.POST:
        form = VideoForm(request.POST,request.FILES, instance = video)
        if form.is_valid():
            dadus = form.save(commit=False)
            dadus.save()
            messages.success(request,"Dadus Atualiza ho Susessu..!")
            return redirect('video')
    else:
        formulariu = VideoForm(instance = video)
        context = {
            'form' : formulariu
        }
        return render(request, "video/update.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def hamosvideo(request, id):
    video = Video.objects.get(id=id)
    video.delete()
    messages.success(request,"Dadus Apaga  Susessu..!")
    return redirect('video')

def show(request):
     video = Video.objects.all()
     context = {
        "video" : video
        }
     return render(request, "video/show.html", context)



def showvideo(request):
    lingua = request.LANGUAGE_CODE
    if lingua == "en":
        first_three_video = Video.objects.filter(lingua__id=3).order_by('-id')
    elif lingua == "pt":
        first_three_video = Video.objects.filter(lingua__id=2).order_by('-id')
    elif lingua == "tet":
        first_three_video = Video.objects.filter(lingua__id=1).order_by('-id')
    else:
        first_three_video = Video.objects.filter(lingua__id=3).order_by('-id')

    tinan_list = Video.objects.exclude(datapublikasaun__isnull=True)\
        .annotate(tinan=ExtractYear('datapublikasaun'))\
        .values_list('tinan', flat=True).distinct().order_by('-tinan')

    context = {
        "video": first_three_video,
        "tinan_list": tinan_list,
    }
    return render(request, "video/showvideo.html", context)


