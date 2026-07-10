from django.shortcuts import render,redirect
from django import template
import base64


from main.utils import *

register = template.Library()

@register.filter
def encrypt_id_tag(id_encrypt):
    return encrypt_id(id_encrypt)

@register.filter
def decrypt_id_tag(encrypted_id):
        return decrypt_id(encrypted_id)

@register.filter
def get_item(dictionary, key):
    try:
        return dictionary.get(key)
    except AttributeError:
        return None


