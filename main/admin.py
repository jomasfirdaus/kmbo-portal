# portal/admin.py  (ou main/admin.py depende app naran)

from django.contrib import admin
from .models import (
    Lingua, Organograma, Dokumentu, Anunsiu, ParseiruSira, Kategoria, Imajen,
    Notisia, VizaunMisaun, Galeria, Pic, Foto, Video,
    Mensajenhusikordenador, Ekipakmbo, Infojeralkmbo, Finansiamentunoapoiu,
    Publikasaunkmbo, Dokumentusimportantes,
    RegistuPartisipante, RegistuVoluntariu,
    Kontaktu, Kontaktuami,
    Artigu, Atividade, Projetu, RegistuMenbroKmbo
)

# ----------- Utilidade ba preview imajen iha list view -------------
from django.utils.html import format_html

class ImagePreviewMixin:
    def preview(self, obj):
        if hasattr(obj, 'imagen') and obj.imagen:
            return format_html('<img src="{}" style="height:50px;" />', obj.imagen.url)
        if hasattr(obj, 'imajen') and obj.imajen:
            return format_html('<img src="{}" style="height:50px;" />', obj.imajen.url)
        if hasattr(obj, 'image') and obj.image:
            return format_html('<img src="{}" style="height:50px;" />', obj.image.url)
        return "-"
    preview.short_description = "Preview"

# ---------------- ModelAdmin sira -----------------
@admin.register(Lingua)
class LinguaAdmin(admin.ModelAdmin):
    list_display = ("id", "naran")
    search_fields = ("naran",)

@admin.register(Organograma)
class OrganogramaAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ("id", "preview", "lingua")
    list_filter  = ("lingua",)

@admin.register(Notisia)
class NotisiaAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display  = ("id", "titlu", "datapublika", "kategoria", "status", "lingua")
    list_filter   = ("status", "kategoria", "lingua")
    search_fields = ("titlu",)
    ordering      = ("-datapublika",)

@admin.register(Anunsiu)
class AnunsiuAdmin(admin.ModelAdmin):
    list_display  = ("id", "titlu", "datapublikasuan", "dataremata", "lingua")
    list_filter   = ("lingua",)
    date_hierarchy = "datapublikasuan"

@admin.register(Galeria)
class GaleriaAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display  = ("id", "titulu", "preview", "data", "lingua")
    list_filter   = ("lingua",)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("id", "titulu", "datapublikasaun", "lingua")
    list_filter  = ("lingua",)
    search_fields = ("titulu",)

# ---------- Registu Partisipante & Voluntariu -------------
@admin.register(RegistuPartisipante)
class RegistuPartisipanteAdmin(admin.ModelAdmin):
    list_display  = ("naran", "kategoria", "postu", "sexo", "data_rejistu")
    list_filter   = ("kategoria", "postu", "sexo")
    search_fields = ("naran", "email", "telefone")
    date_hierarchy = "data_rejistu"

@admin.register(RegistuVoluntariu)
class RegistuVoluntariuAdmin(admin.ModelAdmin):
    list_display  = ("naran", "area_voluntariadu", "postu", "sexo", "data_rejistu")
    list_filter   = ("area_voluntariadu", "postu", "sexo")
    search_fields = ("naran", "email", "telefone")
    date_hierarchy = "data_rejistu"

# ---------- Projetu -------------
@admin.register(Projetu)
class ProjetuAdmin(admin.ModelAdmin):
    list_display  = ("titlu", "porsentu", "status", "data_inicio", "data_final", "lingua")
    list_filter   = ("status", "lingua")
    search_fields = ("titlu",)
    date_hierarchy = "data_inicio"

# ---------- Resto modelu sira ho setup simples ---------
simple_models = [
    Dokumentu, ParseiruSira, Kategoria, Imajen, VizaunMisaun,
    Pic, Foto, Mensajenhusikordenador, Ekipakmbo, Infojeralkmbo,Finansiamentunoapoiu,
    Publikasaunkmbo, Dokumentusimportantes, Kontaktu, Kontaktuami,
    Artigu, Atividade
]

for mdl in simple_models:
    admin.site.register(mdl)









@admin.register(RegistuMenbroKmbo)
class RegistuMenbroKmboAdmin(admin.ModelAdmin):
    list_display = ('naran_kompletu', 'get_generu_display', 'get_posto_display', 
                   'get_hela_fatin_atual_display', 'get_servisu_hanesan_display', 'data_rejistu')
    list_filter = ('generu', 'posto', 'hela_fatin_atual', 'servisu_hanesan', 'idade')
    search_fields = ('naran_kompletu', 'nomor_eleitoral_bi', 'telefone', 'email')
    list_per_page = 25
    ordering = ('-data_rejistu',)
    
    fieldsets = (
        ('Dadus Pessoal', {
            'fields': ('naran_kompletu', 'idade', 'generu', 'nomor_eleitoral_bi')
        }),
        ('Hela Fatin', {
            'fields': ('hela_fatin_atual', 'posto')
        }),
        ('Edukasaun no Profisaun', {
            'fields': ('habilitasaun_literaria', 'servisu_hanesan', 'fatin_servisu')
        }),
        ('Kontaktu', {
            'fields': ('telefone', 'email')
        }),
    )
    
    def get_servisu_hanesan_display(self, obj):
        return obj.get_servisu_hanesan_display()
    get_servisu_hanesan_display.short_description = 'Servisu'
    
    def get_generu_display(self, obj):
        return obj.get_generu_display()
    get_generu_display.short_description = 'Jéneru'
    
    def get_posto_display(self, obj):
        return obj.get_posto_display()
    get_posto_display.short_description = 'Postu'
    
    def get_hela_fatin_atual_display(self, obj):
        return obj.get_hela_fatin_atual_display()
    get_hela_fatin_atual_display.short_description = 'Hela Fatin'