from django.shortcuts import redirect
from django.utils.translation import activate
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from main.models import *

def set_language(request):
    language_code = request.GET.get('language')
    valid_language_codes = [code for code, _ in settings.LANGUAGES]

    if language_code in valid_language_codes:
        request.session['selected_language'] = language_code
        activate(language_code)
    selected_language = request.session.get('selected_language', settings.LANGUAGE_CODE)
    print(f"Selected language: {selected_language}")  

    return redirect(request.META.get('HTTP_REFERER'))
