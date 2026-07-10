from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User

class Rejistu(models.Model):
    naran = models.CharField(max_length=250, null=True, blank=True, verbose_name="Naran")
    email = models.EmailField(max_length=250, null=True, blank=True, verbose_name="Email")
    kontaktu = models.IntegerField(null=True, blank=True, verbose_name="Kontaktu")
    pozisaun = models.CharField(max_length=250, null=True, blank=True, verbose_name="Pozisaun")
    fotografia = models.ImageField(upload_to='imajenmedia/', default='imagenfunsionariu/default.png', null=True, blank=True, verbose_name="Foto")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Level User")
    def __str__(self):
        return f"{self.naran} {self.email} {self.kontaktu} {self.pozisaun} {self.user}"
