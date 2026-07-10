from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import VizaunMisaun
from .forms import VizaunMisaunForm
from django.contrib import messages
from main.utils import *
from main.decorators import allowed_users

@login_required
@login_required
def vizaunmisaun(request):
    vm = VizaunMisaun.objects.all().order_by('-id')
    context = {
        "vm": vm,
    }    
    return render(request, "Vizaun_misaun/lista.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def updatevm(request, id):
    ide=decrypt_id(id)
    vm = get_object_or_404(VizaunMisaun, id=ide)
    if request.method == 'POST':
        form = VizaunMisaunForm(request.POST, request.FILES, instance=vm)
        if form.is_valid():
            form.save()
            messages.success(request, "Dadus Atualiza ho Susessu..!")
            return redirect('listavm')
        else:
            messages.error(request, "Ada kesalahan dalam form, silakan periksa kembali.")
    else:
        form = VizaunMisaunForm(instance=vm)
    
    context = {
        'form': form
    }
    return render(request, "Vizaun_misaun/update.html", context)







# def vizaunmisaun(request):
#     vm = VizaunMisaun.objects.all()
#     first_three_vm = vm.order_by('-id')
   
#     context = {
#         "vm" : first_three_vm
#         }
   
#     return render(request, "Vizaun_misaun/lista.html", context)


# # def inputvm(request):
# #     if request.POST:
# #         forms = VizaunMisaunForm(request.POST, request.FILES)
# #         if forms.is_valid():
# #             dadus = forms.save(commit=False)
# #             dadus.save()
# #             messages.success(request,"Dados Rejistu  ho Susessu..!")
# #             return redirect('listavm')
# #     else:
# #         formulariu = VizaunMisaunForm()
# #         context ={
            
# #             'form': formulariu}

# #     return render(request, "Vizaun_misaun/input.html", context)

# def updatevm(request, id):
#     vm = VizaunMisaun.objects.get(id=id)
#     if request.POST:
#         form = VizaunMisaunForm(request.POST,request.FILES, instance = vm)
#         if form.is_valid():
#             dadus = form.save(commit=False)
#             dadus.save()
#             messages.success(request,"Dadus Atualiza ho Susessu..!")
#             return redirect('listavm')
#     else:
#         formulariu = VizaunMisaunForm(instance = vm)
#         context = {
#             'form' : formulariu
#         }
#         return render(request, "Vizaun_misaun/update.html", context)

# # def hamosvm(request, id):
# #     vm = VizaunMisaun.objects.get(id=id)
# #     vm.delete()
# #     messages.success(request,"Dadus Apaga  Susessu..!")
# #     return redirect('listavm')

def show(request):
    vizaunmisaun = VizaunMisaun.objects.all()
    lingua = request.LANGUAGE_CODE
    if lingua=="en" :
        vizaunmisaun=VizaunMisaun.objects.filter(lingua__id=3)
    elif lingua=="pt":
        vizaunmisaun=VizaunMisaun.objects.filter(lingua__id=2)
    elif lingua=="tet":
        vizaunmisaun=VizaunMisaun.objects.filter(lingua__id=1)
   
    context = {
        "vizaunmisaun" : vizaunmisaun
        }
    return render(request, "Vizaun_misaun/show.html",context)

