from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from portal.models import *
from .forms import RejistuForm, CustomPasswordChangeForm
from .forms import RejistuForm, CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from .utils import split_string
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, auth
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from main.decorators import allowed_users


@login_required
@allowed_users(allowed_roles=['admin'])
def uzuariu(request):
    uzuariu = Rejistu.objects.all()
    first_uzuariu = uzuariu.order_by('-id')
    context={
        'uzuariu': first_uzuariu
    }
    return render(request, "perfil/lista.html", context)

@login_required
@allowed_users(allowed_roles=['admin'])
def rejistuuzuariu(request):
    if request.method == "POST":
        form = RejistuForm(request.POST, request.FILES, user=request.user)  # Passando user
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = email  # Use email as username
            password = form.cleaned_data.get('password1')  # Get the password from the form
            # Check if the email (used as username) already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Email ne'e iha tiha ona. Favor hili email seluk.")
                return redirect('rejistuuzuariu')
            # Create a new user if email is unique
            user = User(username=username, email=email)
            user.set_password(password)  # Set the password securely
            user.save()
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            # Add the user to the selected group
            group_user = Group.objects.get(name=form.cleaned_data.get('group_name'))
            user.groups.add(group_user)
            messages.success(request, 'Rejistu Uzuariu ho susesu!.')
            return redirect('uzuariu')
    else:
        form = RejistuForm(user=request.user)  # Passando user
    context = {
        'uzuariu': form
    }
    return render(request, 'perfil/rejistu_uzuariu.html', context)

@login_required
@allowed_users(allowed_roles=['admin'])
def update_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Update the session to prevent the user from being logged out
            messages.success(request, 'Ita-nia senha atuáliza ho susesu.')
            return redirect('perfil')  # Redirect to the appropriate view after successful password change
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'perfil/update_password.html', {'form': form})

@login_required
@allowed_users(allowed_roles=['admin'])
def updatedadus(request):
    user_profile = get_object_or_404(Rejistu, user=request.user)

    if request.method == 'POST':
        form = RejistuForm(request.POST, request.FILES, instance=user_profile, user=request.user)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Atualiza Profile Ho Succesu.')
            return redirect('perfil')
    else:
        form = RejistuForm(instance=user_profile, user=request.user)

    context = {
        'form': form
    }
    return render(request, 'perfil/update_dadus.html', context)

@login_required
@allowed_users(allowed_roles=['admin'])
def hamosuzuariu(request, id):
    uzuariu = get_object_or_404(Rejistu, id=id)
    # Primeiro, exclua o objeto Rejistu
    uzuariu.delete()
    # Agora, exclua o usuário
    if uzuariu.user:
        uzuariu.user.delete()  # Hamos tan user iha user model mos
    messages.success(request, "Dadus Apaga susesu!")
    return redirect('uzuariu')

def login(request):
    if request.method == 'POST':
        naran = request.POST['email']
        senha = request.POST['password']
        user = auth.authenticate(request, username=naran, password=senha)

        if user is not None:
            auth.login(request, user)
            
            # Hetan utilizador nia 'Rejistu' nia naran
            rejistu = user.rejistu_set.first()  # Primeiru registu
    
            if rejistu:
                user_naran = rejistu.naran  # Hetan 'naran' hosi 'Rejistu'
            else:
                user_naran = 'Guest'  # Se labele hetan, tau 'Guest'

            # Mensajem susesu ho utilizador nia naran
            messages.success(request, f'Bem-Vindo {user_naran} !')
            return redirect('kmbokudaulun')
        else:
            messages.error(request, 'Username & Password tau lalos')  # Mensagem de erro
            return redirect('login')

    else:
        return render(request, 'perfil/login.html')



@login_required  
def main(request):
    return render(request, "portal/main.html")

@login_required  
def perfil(request):
    user_profile = Rejistu.objects.get(user=request.user)
    context = {
        'user_profile': user_profile
    }
    return render(request, "perfil/perfil.html", context)