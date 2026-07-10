from django.contrib import admin
from .models import Rejistu

class RejistuAdmin(admin.ModelAdmin):
    list_display = ('naran', 'email', 'kontaktu', 'pozisaun', 'user')
    search_fields = ('naran', 'email', 'pozisaun', 'user__username')
    list_filter = ('pozisaun',)

admin.site.register(Rejistu, RejistuAdmin)
