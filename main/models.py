from typing import Iterable, Optional
import os
from django.db import models
from ckeditor.fields import RichTextField
from embed_video.fields import EmbedVideoField
from tinymce.models import HTMLField
from django.utils import timezone
from django.utils.text import slugify
# Hahu Update Husi ne'e...!
import qrcode
from io import BytesIO
from django.core.files import File





def default_pdf_path():
    return os.path.join('filepdf', 'pdf_mamuk.pdf')

class Lingua(models.Model):
    naran = models.CharField(max_length=100,null=True, blank=True, verbose_name="Lingua")
   
    def __str__(self):
        return "{}".format(self.naran) 
    
class Organograma(models.Model):
    imajen = models.ImageField(upload_to='jorganograma/', default='jorganograma/default.png',null=True, blank=True )
    lingua=models.ForeignKey(Lingua, on_delete=models.PROTECT,null=False, default="", blank=False, verbose_name = "Hili lingua")

    def save(self):
        super().save()
    def _str_(self):
        return " {}".format(self.imajen, self.lingua)

class Dokumentu(models.Model):
    file = models.ImageField(upload_to='kmbo_doc/')
    def __str__(self):
         return "{}".format( self.file)       

class Anunsiu(models.Model):
    titlu = models.CharField(max_length=250, null=True, blank=True)
    deskrisaun = models.TextField(max_length=250, null=True, blank=True)
    datapublikasuan = models.DateTimeField(verbose_name="Data Publikasuan", null=True, blank=True)  # Verifique se o nome está correto
    dataremata = models.DateTimeField(verbose_name="Data Remata", null=True, blank=True)  # Verifique se o nome está correto
    dokumentu = models.ManyToManyField('Dokumentu')
    lingua = models.ForeignKey(Lingua, on_delete=models.PROTECT, null=False, blank=False, verbose_name="Hili lingua")

    def save(self, *args, **kwargs):
        super(Anunsiu, self).save(*args, **kwargs)

    def __str__(self):
        return "{} - {}".format(self.titlu, self.datapublikasuan)

class ParseiruSira(models.Model):
    titlu = models.CharField(max_length=250,null=True,blank=True)
    imagen = models.ImageField(upload_to='imagenparseirusira/', default='imagenparseiruweb/default.png',null=True, blank=True )
    link_site = models.URLField(max_length=250,null=True,blank=True)
    lingua=models.ForeignKey(Lingua, on_delete=models.PROTECT,null=False, blank=False, verbose_name = "Hili lingua")

    def save(self):
        super().save()
    def __str__(self):
        return " {}".format(self.titlu,self.imagen,self.link_site)
    
class Kategoria(models.Model):
    naran = models.CharField(max_length=250, null=True, blank=True) 
    slug = models.SlugField(max_length=255, unique=True, null=False)

    def __str__(self):
        return " {}".format(self.naran)  
    
    def get_slug_source(self):
        # Default Title
        return getattr(self, 'naran', None)

    def save(self, *args, **kwargs):
        if not self.slug:
            source = self.get_slug_source()
            if source:
                self.slug = slugify(source)
        super().save(*args, **kwargs)
    
class Imajen(models.Model):
    titlu = models.CharField(max_length=250,null=True,blank=True)
    image = models.ImageField(upload_to='geleri/', default='imageimagen/default.png',null=True, blank=True, verbose_name="Imajen")

    def __str__(self):
        return "{}.".format(self.titlu, self.image)  
    
STATUS_CHOICES = [
    ("Pendente", "Pendente"),
    ("Review", "Review"),
    ("Publika", "Publika")
]
class Notisia(models.Model):
    datapublika=models.DateField(max_length=50, null=True, blank=True, verbose_name="Data Publikasaun")
    kategoria=models.ForeignKey(Kategoria,on_delete=models.PROTECT,null=True, blank=True, verbose_name = "Hili kategoria")
    imajen=models.ForeignKey(Imajen, on_delete=models.PROTECT,null=True, blank=True, verbose_name = "Imajen")
    titlu = models.CharField(max_length=250, null=True, blank=True, verbose_name = "Titlu") 
    konteudu = RichTextField(null=True, blank=True, verbose_name = "Konteudu") 
    status = models.TextField(max_length=250, null=True, blank=True, verbose_name = "Status", choices=STATUS_CHOICES)
    lingua=models.ForeignKey(Lingua, on_delete=models.PROTECT,null=False, blank=False, verbose_name = "Hili lingua")
    slug = models.SlugField(max_length=255, unique=True, null=False)
    
    def __str__(self):
        return "{}. {}".format(self.datapublika,self.kategoria,self.imajen, self.titlu,self.lingua ,self.konteudu, self.status)  
    
    def get_slug_source(self):
        # Default Title
        return getattr(self, 'titlu', None)

    def save(self, *args, **kwargs):
        if not self.slug:
            source = self.get_slug_source()
            if source:
                self.slug = slugify(source)
        super().save(*args, **kwargs)

class VizaunMisaun(models.Model):
    vizaun = RichTextField(null=True, blank=True, verbose_name = "Vizaun")
    misaun = RichTextField(null=True, blank=True, verbose_name = "Misaun")
    historia = RichTextField(null=True, blank=True, verbose_name = "historia")
    objetivuprincipal = RichTextField(null=True, blank=True, verbose_name = "objetivuprincipal")
    lingua=models.ForeignKey(Lingua, on_delete=models.PROTECT,null=False, blank=False, verbose_name = "Hili lingua")

    def __str__(self):
        return "{} {}".format(self.vizaun, self.misaun, self.historia, self.objetivuprincipal) 

class Galeria(models.Model): 
    titulu = models.CharField(max_length=500,null=True, blank=True, verbose_name="Titulu")
    cover = models.ImageField(upload_to='geleri/', default='imagej/default.png',null=True, blank=True, verbose_name="Imajen")
    lingua=models.ForeignKey(Lingua, on_delete=models.PROTECT,null=False, blank=False, verbose_name = "Hili lingua")
    data = models.DateField(null=True, blank=True, verbose_name="Data Publikasaun")

    def __str__(self):
        return "{} {}".format(self.titulu, self.cover) 
    
class Pic(models.Model):
    pic = models.ImageField(upload_to='kmbo_img/')
    def __str__(self):
         return "{}".format( self.pic)

class Foto(models.Model):
    galeria=models.ForeignKey(Galeria, on_delete=models.PROTECT,null=True, blank=True, verbose_name = "Galeria")
    foto = models.ManyToManyField('Pic')

    def __str__(self):
        return "{} {}".format(self.galeria, self.foto) 
    
class Video(models.Model):
    titulu = models.CharField(max_length=500,null=True, blank=True, verbose_name="Titulu")
    link = EmbedVideoField(verbose_name="Link")
    datapublikasaun = models.DateField(null=True, blank=True, verbose_name="Data Publikasaun")
    lingua=models.ForeignKey(Lingua, on_delete=models.PROTECT,null=False, blank=False, verbose_name = "Hili lingua")

    def __str__(self):
        return "{} {}".format(self.titulu, self.link, self.datapublikasaun) 
    
#Foun=================================================================================================================
class Mensajenhusikordenador(models.Model):
    naran = models.CharField(max_length=250,null=True,blank=True)
    pozisaun = models.CharField(max_length=250,null=True,blank=True)
    imajen = models.ImageField(upload_to='jMensajenhusikordenador/', default='jMensajenhusikordenador/default.png',null=True, blank=True )
    lingua=models.ForeignKey(Lingua, on_delete=models.PROTECT,null=False, default="", blank=False, verbose_name = "Hili lingua")
    deskrisaun = RichTextField(null=True, blank=True, verbose_name = "deskrisaun")
    

    def save(self):
        super().save()
    def _str_(self):
        return " {}".format(self.imajen, self.lingua)

class Ekipakmbo(models.Model):
    naran = models.CharField(max_length=250,null=True,blank=True)
    pozisaun = models.CharField(max_length=250,null=True,blank=True)
    imajen = models.ImageField(upload_to='jMensajenhusikordenador/', default='jMensajenhusikordenador/default.png',null=True, blank=True )
    lingua=models.ForeignKey(Lingua, on_delete=models.PROTECT,null=False, default="", blank=False, verbose_name = "Hili lingua")
    deskrisaun = RichTextField(null=True, blank=True, verbose_name = "deskrisaun")

    def save(self):
        super().save()
    def _str_(self):
        return " {}".format(self.imajen, self.lingua)
    

class Infojeralkmbo(models.Model):
    titlu = models.CharField(max_length=250,null=True,blank=True)
    imajen = models.ImageField(upload_to='jinfojeralkmbo/', default='jinfojeralkmbo/default.png',null=True, blank=True )
    lingua=models.ForeignKey(Lingua, on_delete=models.PROTECT,null=False, default="", blank=False, verbose_name = "Hili lingua")
    deskrisaun = RichTextField(null=True, blank=True, verbose_name = "deskrisaun")

    def save(self):
        super().save()
    def _str_(self):
        return " {}".format(self.imajen, self.lingua)

class BaseContentModel(models.Model):
    titlu = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        verbose_name=("Títulu")
    )
    deskrisaun  = RichTextField(null=True, blank=True, verbose_name = "Deskrisaun")
    
    file_pdf = models.FileField(upload_to='filepdf/', null=False, blank=False)
    
    lingua = models.ForeignKey(
        Lingua,
        on_delete=models.PROTECT,
        verbose_name=("Lingua")
    )

    class Meta:
        abstract = True
        # ordering = ['-postdate']misaun
    
    def __str__(self):
        return self.titlu or str(("Sem Títulu"))
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class Finansiamentunoapoiu(BaseContentModel):
    class Meta(BaseContentModel.Meta):
        verbose_name = ("Finansiamentu no Apoiu")
        verbose_name_plural = ("Finansiamentu no Apoiu")

class Publikasaunkmbo(BaseContentModel):
    class Meta(BaseContentModel.Meta):
        verbose_name = ("Publikasaun KMBO")
        verbose_name_plural = ("Publikasaun KMBO")

class Dokumentusimportantes(BaseContentModel):
    class Meta(BaseContentModel.Meta):
        verbose_name = ('Dokumentus Importantes')
        verbose_name_plural = ("Dokumentus Importantes")



class RegistuPartisipante(models.Model):
    # Postu (sub-distritu) sira iha Bobonaro
    POSTU_BOBONARO = [
        ('atabae', 'Atabae'),
        ('balibo', 'Balibo'),
        ('bobonaro', 'Bobonaro'),
        ('cailaco', 'Cailaco'),
        ('lolotoe', 'Lolotoe'),
        ('maliana', 'Maliana'),
    ]

    # Kategoria partisipante sira nian
    KATEGORIA_PARTISIPANTE = [
        ('estudante', 'Estudante'),
        ('profisional', 'Profisionál'),
        ('empresariu', 'Empresáriu'),
        ('funsionariu', 'Funsionáriu Públiku'),
        ('seluk', 'Seluk'),
    ]

    # DADUS PARTISIPANTE
    no_eleitoral = models.CharField(max_length=100, verbose_name="No. Eleitoral (ID Uniku)", unique=True)
    naran = models.CharField(max_length=250, verbose_name="Naran Kompletu")
    fotografia = models.ImageField(upload_to='partisipante/foto/', blank=True, null=True, verbose_name="Fotografia Atual")
    sexo = models.CharField(max_length=10, choices=[('M', 'Mane'), ('F', 'Feto')], verbose_name="Sexo")
    data_moris = models.DateField(verbose_name="Data Moris", blank=True, null=True)
    pozisaun = models.CharField(max_length=250, verbose_name="Pozisaun iha KMBO", blank=True)

    kategoria = models.CharField(
        max_length=50,
        choices=KATEGORIA_PARTISIPANTE,
        verbose_name="Kategoria Partisipante"
    )

    naran_instituisaun = models.CharField(max_length=250, verbose_name="Naran Instituisaun", blank=True)
    telefone = models.CharField(max_length=20, verbose_name="Numeru Telefone", blank=True)
    email = models.EmailField(blank=True, null=True, verbose_name="Email")

    postu = models.CharField(
        max_length=100,
        choices=POSTU_BOBONARO,
        verbose_name="Postu Administrativu"
    )

    suku = models.CharField(max_length=150, verbose_name="Suku", blank=True)
    aldeia = models.CharField(max_length=150, verbose_name="Aldeia", blank=True)

    munucipio = models.CharField(
        max_length=100,
        default="Bobonaro",
        editable=False,
        verbose_name="Rezidensial Munisípiu Atual"
    )

    data_rejistu = models.DateTimeField(auto_now_add=True, verbose_name="Data Rejistu")

    def save(self, *args, **kwargs):
        self.munucipio = "Bobonaro"  # Garante munisipiu sei "Bobonaro"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.naran} - {self.kategoria} ({self.postu})"

    class Meta:
        verbose_name = "Partisipante"
        verbose_name_plural = "Partisipante sira"
        ordering = ['-data_rejistu', 'naran']




class RegistuVoluntariu(models.Model):
    # Postu (sub-distritu) sira iha Bobonaro
    POSTU_BOBONARO = [
        ('atabae', 'Atabae'),
        ('balibo', 'Balibo'),
        ('bobonaro', 'Bobonaro'),
        ('cailaco', 'Cailaco'),
        ('lolotoe', 'Lolotoe'),
        ('maliana', 'Maliana'),
    ]
    
    # Area voluntariadu sira nian
    AREA_VOLUNTARIADU = [
        ('edu', 'Edukasaun'),
        ('saude', 'Saude'),
        ('agri', 'Agricultura'),
        ('juv', 'Juventude'),
        ('gender', 'Jeneru'),
        ('outro', 'Outro'),
    ]
    
    naran = models.CharField(max_length=250, verbose_name="Naran kompletu")
    sexo = models.CharField(max_length=10, choices=[('M', 'Manes'), ('F', 'Feto')], verbose_name="Sexo")
    data_moris = models.DateField(verbose_name="Data Moris")
    pozisaun = models.CharField(max_length=250, verbose_name="Pozisaun")
    
    # Automatiku set munucipiu ba Bobonaro
    munucipio = models.CharField(
        max_length=100, 
        default="Bobonaro", 
        editable=False,
        verbose_name="Munucipio"
    )
    
    postu = models.CharField(
        max_length=100, 
        choices=POSTU_BOBONARO, 
        verbose_name="Postu (Bobonaro)"
    )
    
    area_voluntariadu = models.CharField(
        max_length=50,
        choices=AREA_VOLUNTARIADU,
        verbose_name="Area Voluntariadu"
    )
    
    lingua = models.ForeignKey(
        'Lingua', 
        on_delete=models.PROTECT, 
        verbose_name="Lingua ne'ebe domina"
    )
    
    telefone = models.CharField(max_length=20, verbose_name="Numeru Telefone")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    
    deskrisaun = HTMLField(blank=True, null=True, verbose_name="Deskrisaun kona-ba esperiensia")
    
    data_rejistu = models.DateTimeField(auto_now_add=True, verbose_name="Data Rejistu")
    
    def save(self, *args, **kwargs):
        self.munucipio = "Bobonaro"  # Garante munucipiu sempre Bobonaro
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.naran} - {self.area_voluntariadu} ({self.postu})"

    class Meta:
        verbose_name = "Voluntariu"
        verbose_name_plural = "Voluntariu sira"
        ordering = ['-data_rejistu', 'naran']

class Kontaktu(models.Model):
    naran=models.CharField(max_length=250,null=True,blank=True, verbose_name="Naran")
    email=models.CharField(max_length=250,null=True,blank=True, verbose_name="Email")
    numeru = models.IntegerField(null=True, blank=True, verbose_name="No.Tlf")
    asuntu=models.CharField(max_length=250,null=True,blank=True, verbose_name="Asuntu")
    mensajen=RichTextField(null=True,blank=True, verbose_name="Mensajen")
    
    def save(self):
        super().save()
    def __str__(self):
        return " {}".format(self.naran,self.email, self.asuntu,self.mensajen)
    
class Kontaktuami(models.Model):
    lokalizasaun = RichTextField(null=True, blank=True, verbose_name="Lokalizasaun")
    sukursal = RichTextField(null=True, blank=True, verbose_name="Sukursal")
    website = models.CharField(max_length=250, null=True, blank=True, verbose_name="Website")
    email = models.CharField(max_length=250, null=True, blank=True, verbose_name="Email")
    numerutelemovel = models.CharField(max_length=250, null=True, blank=True, verbose_name="No.Tlf")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.lokalizasaun} | {self.email} | {self.numerutelemovel}"


class Artigu(models.Model):
    titlu = models.CharField(max_length=250, null=True, blank=True)
    deskrisaun = models.TextField(max_length=250, null=True, blank=True)
    file_pdf = models.FileField(upload_to='filepdf/', null=False, blank=False)
    data = models.DateField(verbose_name="Data", null=True, blank=True, default=timezone.now)
    lingua = models.ForeignKey(Lingua, on_delete=models.PROTECT, null=False, blank=False, verbose_name="Hili lingua")

    def __str__(self):
        return self.titlu or "Artigu Tanba Títulu la iha"  

class Atividade(models.Model):
    titlu = models.CharField(max_length=250, null=True, blank=True)
    deskrisaun = RichTextField(null=True, blank=True, verbose_name = "deskrisaun")
    lingua = models.ForeignKey(Lingua, on_delete=models.PROTECT, null=False, blank=False, verbose_name="Hili lingua")

    def __str__(self):
        return self.titlu or "Artigu Tanba Títulu la iha"

class Projetu(models.Model):
    STATUS_CHOICES = [
        ('prosesu', 'Iha Prosesu'),
        ('kumpri', 'Kumpri'),
    ]

    titlu = models.CharField(max_length=250, null=True, blank=True)
    deskrisaun = models.TextField(max_length=250, null=True, blank=True)
    
    data_inicio = models.DateField(null=True, blank=True)
    data_final = models.DateField(null=True, blank=True)

    porsentu = models.PositiveIntegerField(
        default=0,
        help_text="0-99% = iha prosesu; 100% = kumpri"
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='prosesu'
    )

    lingua = models.ForeignKey(
        'Lingua',
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        verbose_name="Hili lingua"
    )

    def __str__(self):
        return self.titlu or "Projetu Tanba Títulu la iha"

    def save(self, *args, **kwargs):
        if self.porsentu == 100:
            self.status = 'kumpri'
        else:
            self.status = 'prosesu'
        super().save(*args, **kwargs)









MUNICIPIOS_TIMOR_LESTE = [
    ('DILI', 'Dili'),
    ('BOBONARO', 'Bobonaro'),
    ('LIQUICA', 'Liquiçá'),
    ('BAUCAU', 'Baucau'),
    ('COVALIMA', 'Covalima'),
    ('LAUTEM', 'Lautém'),
    ('VIQUEQUE', 'Viqueque'),
    ('MANATUTO', 'Manatuto'),
    ('MANUFAHI', 'Manufahi'),
    ('AINARO', 'Ainaro'),
    ('ERMERA', 'Ermera'),
    ('RAEOA', 'Oé-Cusse (RAEOA)'),
    ('ATAURO', 'Ataúro'),
    ('SELUK', 'Seluk'),
]

IDADE_CHOICES = [
    ('16-30', '16-30'),
    ('31-45', '31-45'),
    ('46-55', '46-55'),
    ('56-70', '56-70'),
    ('71+', '71+'),
]

GENERU_CHOICES = [
    ('FETO', 'Feto'),
    ('MANE', 'Mane'),
]

POSTO_CHOICES = [
    ('ATABAE', 'Atabae'),
    ('BALIBO', 'Balibo'),
    ('BOBONARO', 'Bobonaro'),
    ('CAILACO', 'Cailaco'),
    ('MALIANA', 'Maliana'),
    ('LOLOTOE', 'Lolotoe'),
    ('SELUK', 'Seluk/Feto foun ou Mane Foun'),
]

HABILITASAUN_CHOICES = [
    ('SD', 'SD'),
    ('SMP', 'SMP'),
    ('SMA', 'SMA'),
    ('S1', 'S1'),
    ('S2', 'S2'),
    ('S3', 'S3'),
    ('SELUK', 'Seluk (Kursu Especialidade hanesan Mekanika, Operador, Sofer, Soldador, Badaen Fatuk, Badaen Ai. Pescador, Nst)'),
    
]

SERVISU_CHOICES = [
    ('GOVERNU', 'Governu (Ministerius, Instituisaun Autonomo sira EP-IP)'),
    ('LAOS_GOVERNU', 'Laos Governu (NGO Local, International, Embaixada sira)'),
    ('POLISIA_FDTL', 'Polisia/F-FFDTL'),
    ('DOUTOR', 'Doutores ou Medico sira (Geral ou Especialidade)'),
    ('DOSENTE', 'Dosente iha Universidade'),
    ('PROFESOR', 'Profesores (EB, ES no EV)'),
    ('GOVERNNANTE', 'Governnante e Reprezentante Povo (Membru do Governo, Embaixador/a, Deputadu/da  (ativu no eis)'),
    ('SETOR_PRIVADO', 'Setor Privado (Emprezariu/Emprezaria no tekniku especializadu)'),
    ('REFORMADO', 'Reformado (Funsionariu, FDTL, POLISIA nst)'),
    ('TRABLHADOR', 'Trablhador Estranjeiru (Europa, Australia, Korea, Canada,Nst)')
]

FATIN_SERVISU_CHOICES = [
    ('MUNISIPAL', 'Munisipal'),
    ('NASIONAL', 'Nasional'),
    ('EUROPA', 'Europa'),
    ('KOREA', 'Korea'),
    ('AUSTRALIA', 'Australia'),
    ('NEW ZELANDIA', 'New Zelandia'),
    ('SELUK', 'Seluk'),
]

class RegistuMenbroKmbo(models.Model):
    # Dadus Pessoais
    naran_kompletu = models.CharField('Naran Kompletu', max_length=200)
    
    idade = models.CharField(
        'Idade', 
        max_length=10, 
        choices=IDADE_CHOICES
    )
    
    generu = models.CharField(
        'Generu', 
        max_length=10, 
        choices=GENERU_CHOICES
    )
    
    nomor_eleitoral_bi = models.CharField(
        'Nomor Eleitoral OU BI', 
        max_length=50,
        blank=False,  # Muda ba obrigatóriu
        null=False,
        unique=True  # Aumenta unique constraint atu prevene duplikasaun
    )
    
    # Hela Fatin Atual
    hela_fatin_atual = models.CharField(
        'Hela fatin Atual', 
        max_length=50, 
        choices=MUNICIPIOS_TIMOR_LESTE,
        default='DILI'
    )
    
    posto = models.CharField(
        'Posto', 
        max_length=50, 
        choices=POSTO_CHOICES
    )
    
    # Edukasaun no Profisaun
    habilitasaun_literaria = models.CharField(
        'Habilitasaun Literaria', 
        max_length=20, 
        choices=HABILITASAUN_CHOICES
    )
    
    servisu_hanesan = models.CharField(
        'Servisu hanesan', 
        max_length=30, 
        choices=SERVISU_CHOICES
    )
    
    fatin_servisu = models.CharField(
        'Fatin servisu', 
        max_length=20, 
        choices=FATIN_SERVISU_CHOICES,
        default='MUNISIPAL'
    )
    
    # Kontaktu (opsional)
    telefone = models.CharField('Telefone', max_length=30, blank=True, null=True)
    email = models.EmailField('Email', blank=True, null=True)
    
    # Aumenta kampu foun atu marka tipu dokumentu
    tipu_dokumentu = models.CharField(
        'Tipu Dokumentu',
        max_length=20,
        choices=[
            ('ELEITORAL', 'Kartaun Eleitoral'),
            ('BI', 'Bilhete Identidade'),
        ],
        blank=True,
        null=True,
        editable=False  # Labele edit manual
    )
    
    # Meta dados
    data_rejistu = models.DateTimeField('Data Rejistu', auto_now_add=True)
    data_atualizasaun = models.DateTimeField('Data Atualizasaun', auto_now=True)
    
    class Meta:
        verbose_name = 'Membro KMBO'
        verbose_name_plural = 'Membro KMBO Sira'
        ordering = ['-data_rejistu']
        indexes = [
            models.Index(fields=['nomor_eleitoral_bi']),
            models.Index(fields=['tipu_dokumentu']),
            models.Index(fields=['naran_kompletu']),
        ]
    
    def __str__(self):
        return f"{self.naran_kompletu} - {self.get_hela_fatin_atual_display()}"
    
    def save(self, *args, **kwargs):
        # Detekta tipu dokumentu bazeia ba formatu nomor
        if self.nomor_eleitoral_bi:
            # Verifika formatu: ELEITORAL normalmente numeru deit, BI normalmente iha letra
            if self.nomor_eleitoral_bi.isdigit():
                self.tipu_dokumentu = 'ELEITORAL'
            else:
                self.tipu_dokumentu = 'BI'
        super().save(*args, **kwargs)