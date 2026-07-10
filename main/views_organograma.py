from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import OrganogramaForm
from django.contrib import messages
from main.utils import *
from main.decorators import allowed_users

@login_required
@allowed_users(allowed_roles=['admin'])
def listaorganograma(request):
    organograma = Organograma.objects.all()
    first_organograma = organograma.order_by('-id')
    context = {
        "organograma" : first_organograma
        }
    
    return render(request, "organograma/lista.html", context)


# def inputorganograma(request):
#    if request.method=='POST':
#         forms = OrganogramaForm(request.POST,request.FILES)
#         if forms.is_valid():
#             dadus = forms.save(commit=False)
#             dadus.save()
#             messages.success(request,"Dados Rejistu  ho Susessu..!")
#             return redirect('listaorganograma')
#    else:
#         formulariu = OrganogramaForm()
#         context ={
            
#             'form': formulariu}

#    return render(request, "organograma/input.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def updateorganograma(request, id):
    ide=decrypt_id(id)
    organograma = Organograma.objects.get(id=ide)
    if request.method == 'POST':
        form = OrganogramaForm(request.POST, request.FILES, instance=organograma)
        if form.is_valid():
            form.save()
            messages.success(request, "Dadus Atualiza ho Susessu..!")
            return redirect('listaorganograma')
    else:
        formulariu = OrganogramaForm(instance=organograma)
        context = {
            'form': formulariu,
        }
        return render(request, "organograma/update.html", context)

# def hamosorganograma(request, id):
#     organograma = Organograma.objects.get(id=id)
#     organograma.delete()
#     messages.success(request,"Dadus Apaga  Susessu..!")
#     return redirect('listaorganograma')

def show(request):
    organograma = Organograma.objects.all().order_by('-id')
    lingua = request.LANGUAGE_CODE
    if lingua=="en" :
        organograma=Organograma.objects.filter(lingua__id=3).order_by('-id')
    elif lingua=="pt":
        organograma=Organograma.objects.filter(lingua__id=2).order_by('-id')
    elif lingua=="tet":
        organograma=Organograma.objects.filter(lingua__id=1).order_by('-id')
    context = {
        "organograma" : organograma
        }
    return render(request, "organograma/show.html",context)




