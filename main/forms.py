from django import forms
from django.forms import ModelForm
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML, Field, Div
from crispy_forms.bootstrap import TabHolder,Tab
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML
from django.utils.translation import gettext_lazy as _
from ckeditor.widgets import CKEditorWidget
from multiupload.fields import MultiFileField
from django.forms.widgets import DateInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML
from ckeditor_uploader.widgets import CKEditorUploadingWidget  #e ne'e loos
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML, Fieldset


class OrganogramaForm(forms.ModelForm):
    class Meta:
        model  = Organograma
        fields = ['lingua', 'imajen']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Crispy Forms helper
        self.helper = FormHelper()
        self.helper.form_method  = 'post'
        self.helper.form_id      = 'org_id'
        # importante ba upload imajen
        self.helper.form_enctype = 'multipart/form-data'

        # Layout
        self.helper.layout = Layout(
            Row(
                Column('lingua', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('imajen', css_class='form-group col-md-12 mb-0'),
            ),
            HTML(
                """
                <br>
                <div class="float-right">
                    <button id="org"
                            class="btn btn-secondary m-1"
                            type="submit">
                        <i class="fa fa-save"></i>
                        {% if asaun == 'edit' %} Atualiza {% else %} Rejistu {% endif %}
                    </button>

                    <!-- usa aspas simples iha onclick -->
                    <a class="btn btn-warning m-1"
                       onclick='history.back()'>
                       <span class="btn-label"><i class="fa fa-window-close"></i></span>
                       Kansela
                    </a>
                </div>
                """
            ),
        )


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileFiel(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result
          
class AnunsiuForm(forms.ModelForm):
    dokumentu = MultiFileField(
        label='Seleziona dokumentu',
        required=False,
    )

    class Meta:
        model = Anunsiu
        fields = ['lingua', 'titlu', 'deskrisaun', 'dokumentu', 'datapublikasuan', 'dataremata']

    def __init__(self, *args, **kwargs):
        super(AnunsiuForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'anun_id'
        self.helper.layout = Layout(
            Row(Column('lingua', css_class='form-group col-md-12 mb-0')),
            Row(Column('titlu', css_class='form-group col-md-12 mb-0')),
            Row(Column('deskrisaun', css_class='form-group col-md-12 mb-0')),
            Row(Column('dokumentu', css_class='form-group col-md-12 mb-0')),
            Row(
                Column('datapublikasuan', css_class='form-group col-md-12 mb-0', id='id_datapublika'),
                Column('dataremata', css_class='form-group col-md-6 mb-12', id='id_dataremata'),
            ),
        )
        self.fields['datapublikasuan'].widget = forms.DateInput(
            format='%d/%m/%Y',
            attrs={'type': 'date', 'placeholder': 'dd/mm/yyyy'}
        )
        self.fields['dataremata'].widget = forms.DateInput(
            format='%d/%m/%Y',
            attrs={'type': 'date', 'placeholder': 'dd/mm/yyyy'}
        )

class KategoriaForm(forms.ModelForm):
	class Meta:
		model=Kategoria
		fields=['naran']
	def __init__(self, *args, **kwargs):
		super(KategoriaForm,self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method='post'
		self.helper.form_id='kat_id'
		self.helper.layout = Layout(
		

 			Row(
 			Column('naran', css_class='form-group col-md-12 mb-0'),
 			), 

			 HTML(""" 

 			<br>
 				<div class='float-right'>

 			<button  id = 'not' class="btn btn-sm btn-info" type="submit"><i class="fa fa-save"></i> {% if asaun  == 'edit' %} Atualiza {% else %} Rejistu {% endif %}
 				</button>

 					<a class="btn btn-sm btn-warning" onclick=self.history.back()><span class="btn-label"><i class="fa fa-window-close"></i></span> Kansela</a>		
 				</div>
				
 				""")
				
		)          

class ParseiruSiraForm(forms.ModelForm):
	
	class Meta:
		model=ParseiruSira
		fields=['lingua','titlu','imagen','link_site']
	def __init__(self, *args, **kwargs):
		super(ParseiruSiraForm,self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method='post'
		self.helper.form_id='web_id'
		self.helper.layout = Layout(
			Row(
			Column('lingua', css_class='form-group col-md-12 mb-0'),
			),
			Row(
			Column('titlu', css_class='form-group col-md-12 mb-0'),
			),
			Row(
			Column('imagen', css_class='form-group col-md-12 mb-0'),
			),
			Row(
			Column('link_site', css_class='form-group col-md-12 mb-0'),
			),

			HTML(""" 
			

			<br>
				<div class='float-right'>
				

			<button  id = 'web' class="btn btn-secondary m-1" type="submit"><i class="fa fa-save"></i> {% if asaun  == 'edit' %} Atualiza {% else %} Rejistu {% endif %}
				</button>
				

					<a class="btn btn-warning m-1" onclick=self.history.back()><span class="btn-label"><i class="fa fa-window-close"></i></span> Kansela</a>		
				</div>
				
				""")

		)


class LinguaForm(forms.ModelForm):
	
	class Meta:
		model=Lingua
		fields=['naran']
	def __init__(self, *args, **kwargs):
		super(LinguaForm,self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method='post'
		self.helper.form_id='lingia_id'
		self.helper.layout = Layout(
			Row(
			Column('naran', css_class='form-group col-md-12 mb-0'),
			),

			
			HTML(""" 
			

			<br>
				<div class='float-right'>
				

			<button  id = 'dep' class="btn btn-secondary m-1" type="submit"><i class="fa fa-save"></i> {% if asaun  == 'edit' %} Atualiza {% else %} Rejistu {% endif %}
				</button>
				

					<a class="btn btn-warning m-1" onclick=self.history.back()><span class="btn-label"><i class="fa fa-window-close"></i></span> Kansela</a>		
				</div>
				
				""")

		)

# Foto ba info
class ImajenForm(forms.ModelForm):
    class Meta:
        model = Imajen
        fields = ['titlu', 'image']
        labels = {
            'titlu': 'Titlu Imajen',
            'image': 'Imajen',
        }
        widgets = {
            'titlu': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ImajenForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'img_id'
        self.helper.layout = Layout(
            Row(
                Column(Field('titlu', css_class='form-group col-md-12 mb-0'), css_class='col-md-12'),
                Column(Field('image', css_class='form-group col-md-12 mb-0'), css_class='col-md-12'),
            ),
        )

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')

        if not image and self.instance.pk:  # Ensure we're updating an existing instance
            raise forms.ValidationError("La bele apaga tanba imajen ne'e uza iha Notisia.")

        return cleaned_data



# Notisia
class NotisiaForm(forms.ModelForm):
    class Meta:
        model = Notisia
        fields = ['lingua', 'kategoria', 'imajen', 'titlu', 'konteudu', 'datapublika']

    def __init__(self, *args, **kwargs):
        super(NotisiaForm, self).__init__(*args, **kwargs)
        self.fields['konteudu'].widget = CKEditorWidget()

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'notisia_id'
        self.helper.layout = Layout(
            Row(Column('lingua', css_class='form-group col-md-6 mb-0')),
            Row(Column('kategoria', css_class='form-group col-md-6 mb-0')),
            Row(Column('imajen', css_class='form-group col-md-6 mb-0')),
            Row(Column('datapublika', css_class='form-group col-md-6 mb-0', id='id_datapublika')),
            Row(Column('titlu', css_class='form-group col-md-12 mb-0')),
            Row(Column('konteudu', css_class='form-group col-md-12 mb-0')),
            HTML("""
                <br>
                <div class="button-container text-center">
                    <button class="btn btn-xs btn-info" type="submit" id="submit-btn">
                        <i class="fa fa-save"></i> Submete
                    </button>
                    <a class="btn btn-xs btn-danger" href="javascript:history.back();" id="cancel-btn">
                        <i class="fa fa-close"></i> Kancela
                    </a>
                </div>
            """))

        self.fields['datapublika'].widget = forms.DateInput(attrs={'type': 'date'})



class InfojeralkmboForm(forms.ModelForm):
	deskrisaun = forms.CharField(widget=CKEditorWidget())  # Aktivu CKEditor

	class Meta:
		model = Infojeralkmbo
		fields = ['titlu', 'imajen', 'lingua', 'deskrisaun']

	def __init__(self, *args, **kwargs):
		super(InfojeralkmboForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_id = 'web_id'
		self.helper.layout = Layout(
			Row(
				Column('lingua', css_class='form-group col-md-12 mb-0'),
			),
			Row(
				Column('titlu', css_class='form-group col-md-12 mb-0'),
			),
			Row(
				Column('imajen', css_class='form-group col-md-12 mb-0'),  # CORRIGIDO
			),
			Row(
				Column('deskrisaun', css_class='form-group col-md-12 mb-0'),
			),
			HTML(""" 
				<br>
				<div class='float-right'>
					<button id='mensajenhusikordenador' class="btn btn-secondary m-1" type="submit">
						<i class="fa fa-save"></i> {% if asaun == 'edit' %} Atualiza {% else %} Rejistu {% endif %}
					</button>
					<a class="btn btn-warning m-1" onclick="self.history.back()">
						<span class="btn-label"><i class="fa fa-window-close"></i></span> Kansela
					</a>		
				</div>
			""")
		)

          
class KontaktuForm(forms.ModelForm):
	class Meta:
		model=Kontaktu
		fields=['naran', 'email','numeru', 'asuntu', 'mensajen']
	def __init__(self, *args, **kwargs):
		super(KontaktuForm,self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method='post'
		self.helper.form_id='kont_id'
		self.helper.layout = Layout(
		
			HTML("""
		

        <div class="container">
          <div class="row">
            <div class="col-md-6 form-group">
              <input type="text" name="naran" class="form-control p-2" id="naran" placeholder="Naran / Name, Nome" required>
            </div>
            <div class="col-md-6 form-group mt-4 mt-md-0">
              <input type="email" class="form-control p-2" name="email" id="email" placeholder="Email" required>
            </div>
          </div>
		 <div class="form-group mt-4">
            <input type="number" class="form-control p-2" name="numeru" id="numeru" placeholder="No.Tlf" required>
          </div>
          <div class="form-group mt-4">
            <input type="text" class="form-control p-2" name="asuntu" id="asuntu" placeholder="Asuntu /Affair /Assunto" required>
          </div>
          <div class="form-group mt-4">
            <textarea class="form-control" name="mensajen" id="mensajen" rows="7" placeholder="Mensajen / Mensagem / Message" required></textarea>
          </div>
          <div class="my-3">
          </div>
		</div>
		
"""),
			
			

			HTML(""" 
			

			<br>
				<div class='text-center'>
				

			<button  id = 'kont_id' class="btn btn-secondary m-1 " type="submit" style="background-color: rgb(4, 129, 245); margin-left: 15%; ><i class="fa fa-save"></i> {% if asaun  == 'edit' %} Atualiza {% else %} Submit {% endif %}
				</button>
				

				
				</div>
				
				""")

)


# VizaunMisaunPerfil
class VizaunMisaunForm(forms.ModelForm):
    class Meta:
        model = VizaunMisaun
        fields = ['lingua', 'vizaun', 'misaun', 'historia', 'objetivuprincipal']

    def __init__(self, *args, **kwargs):
        super(VizaunMisaunForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'vm_id'
        self.helper.layout = Layout(
            Row(
                Column('lingua', css_class='form-group col-md-12 mb-0 fro'),
            ),
            Row(
                Column('historia', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('vizaun', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('misaun', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('objetivuprincipal', css_class='form-group col-md-12'),
            ),
           
            HTML("""
                <br>
                <div class="button-container text-center">
                    <button class="btn btn-xs btn-info" type="submit" id="submit-btn">
                        <i class="fa fa-edit"></i> Atualiza
                    </button>
                    <a class="btn btn-xs btn-danger" href="javascript:history.back();" id="cancel-btn">
                        <i class="fa fa-close"></i> Kancela
                    </a>
                </div>
            """)
        )

# Galeria
class GaleriaForm(forms.ModelForm):
    class Meta:
        model = Galeria
        fields = ['lingua', 'titulu', 'cover', 'data']
        labels = {
            'lingua': _('Lingua'),
            'titulu': _('Titulu'),
            'cover': _('Imajen Cover'),
            'data': _('Data Publikasaun'),
        }
        widgets = {
            'lingua': forms.Select(attrs={'class': 'form-control'}),
            'titulu': forms.TextInput(attrs={'class': 'form-control'}),
            'cover': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(GaleriaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'galeria_id'
        self.helper.layout = Layout(
            Row(Column(Field('lingua', css_class='form-group col-md-12 mb-0'), css_class='col-md-12')),
            Row(Column(Field('titulu', css_class='form-group col-md-12 mb-0'), css_class='col-md-12')),
            Row(Column(Field('cover', css_class='form-group col-md-12 mb-0'), css_class='col-md-12')),
            Row(Column(Field('data', css_class='form-group col-md-12 mb-0', id='id_data'), css_class='col-md-12')),
        )

class MultiFileInput(forms.ClearableFileInput):
    """Custom widget for handling multiple file uploads."""
    template_name = 'widgets/multi_file_input.html'  # Create a custom template for multiple file inputs

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['multiple'] = True  # Enable multiple file uploads
        return context

class MultipleFileField(forms.FileField):
    """Custom field for handling multiple file uploads."""
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = MultiFileInput()  # Use the custom widget
        super(MultipleFileField, self).__init__(*args, **kwargs)

# Foto
class FotoForm(forms.ModelForm):
    foto = MultipleFileField(
        label='Hili Foto Sira',
        required=False
    )

    class Meta:
        model = Foto
        fields = ['galeria', 'foto']
        labels = {
            'galeria': 'Galeria',
            'foto': 'Foto Sira',
        }
        widgets = {
            'galeria': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(FotoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'foto_id'
        self.helper.layout = Layout(
            Row(Column(Field('galeria', css_class='form-group col-md-12 mb-0'), css_class='col-md-12')),
            Row(Column(Field('foto', css_class='form-group col-md-12 mb-0'), css_class='col-md-12')),
        )

#VideoForm
class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['lingua', 'titulu', 'link', 'datapublikasaun']
        labels = {
            'lingua': _('Lingua'),
            'titulu': _('Titulu Video'),
            'link': _('Link Video'),
            'datapublikasaun': _('Data Publikasaun'),
        }
        widgets = {
            'lingua': forms.Select(attrs={'class': 'form-control'}),
            'titulu': forms.TextInput(attrs={'class': 'form-control'}),
            'link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Insere Link Video'}),
            'datapublikasaun': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'video_id'
        self.helper.layout = Layout(
            Row(Column(Field('lingua', css_class='form-group col-md-12 mb-0'), css_class='col-md-12')),
            Row(Column(Field('titulu', css_class='form-group col-md-12 mb-0'), css_class='col-md-12')),
            Row(Column(Field('link', css_class='form-group col-md-12 mb-0'), css_class='col-md-12')),
            Row(Column(Field('datapublikasaun', css_class='form-group col-md-12 mb-0', id='id_data'), css_class='col-md-12')),
        )

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML
from .models import Mensajenhusikordenador, Ekipakmbo


class MensajenhusikordenadorForm(forms.ModelForm):
    class Meta:
        model = Mensajenhusikordenador
        fields = ['naran', 'pozisaun', 'imajen', 'lingua', 'deskrisaun']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Row(Column('naran', css_class='form-group col-md-6')),
            Row(Column('pozisaun', css_class='form-group col-md-6')),
            Row(Column('lingua', css_class='form-group col-md-12')),
            Row(Column('imajen', css_class='form-group col-md-12')),
            Row(Column('deskrisaun', css_class='form-group col-md-12')),
            HTML("""
                <br>
                <div class="float-right">
                    <button class="btn btn-secondary m-1" type="submit">
                        <i class="fa fa-save"></i> {% if asaun == 'edit' %} Atualiza {% else %} Rejistu {% endif %}
                    </button>
                    <a class="btn btn-warning m-1" onclick='history.back()'>
                        <i class="fa fa-window-close"></i> Kansela
                    </a>
                </div>
            """)
        )


class EkipakmboForm(forms.ModelForm):
    class Meta:
        model = Ekipakmbo
        fields = ['naran', 'pozisaun', 'imajen', 'lingua', 'deskrisaun']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Row(Column('naran', css_class='form-group col-md-6')),
            Row(Column('pozisaun', css_class='form-group col-md-6')),
            Row(Column('lingua', css_class='form-group col-md-12')),
            Row(Column('imajen', css_class='form-group col-md-12')),
            Row(Column('deskrisaun', css_class='form-group col-md-12')),
            HTML("""
                <br>
                <div class="float-right">
                    <button class="btn btn-secondary m-1" type="submit">
                        <i class="fa fa-save"></i> {% if asaun == 'edit' %} Atualiza {% else %} Rejistu {% endif %}
                    </button>
                    <a class="btn btn-warning m-1" onclick='history.back()'>
                        <i class="fa fa-window-close"></i> Kansela
                    </a>
                </div>
            """)
        )


class AtividadeForm(forms.ModelForm):
    class Meta:
        model = Atividade
        fields = ['lingua', 'titlu', 'deskrisaun']

    def __init__(self, *args, **kwargs):
        super(AtividadeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'atividade_form'

        self.helper.layout = Layout(
            Row(
                Column('lingua', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('titlu', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('deskrisaun', css_class='form-group col-md-12 mb-0'),
            ),
            HTML("""
                <br>
                <div class='float-right'>
                    <button id='atividade_submit' class="btn btn-secondary m-1" type="submit">
                        <i class="fa fa-save"></i> {% if asaun == 'edit' %} Atualiza {% else %} Rejistu {% endif %}
                    </button>
                    <a class="btn btn-warning m-1" onclick="self.history.back()">
                        <span class="btn-label"><i class="fa fa-window-close"></i></span> Kansela
                    </a>
                </div>
            """)
        )



class ProjetuForm(forms.ModelForm):
    class Meta:
        model = Projetu
        fields = ['lingua', 'titlu', 'deskrisaun', 'porsentu', 'data_inicio', 'data_final']

        widgets = {
            'deskrisaun': forms.Textarea(attrs={'rows': 4}),
            'porsentu': forms.NumberInput(attrs={'min': 0, 'max': 100}),
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_final': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProjetuForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'projetu_form'

        self.helper.layout = Layout(
            Row(
                Column('lingua', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('titlu', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('deskrisaun', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('porsentu', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('data_inicio', css_class='form-group col-md-6 mb-0'),
                Column('data_final', css_class='form-group col-md-6 mb-0'),
            ),
            HTML("""
                <br>
                <div class='float-right'>
                    <button id='projetu_submit' class="btn btn-secondary m-1" type="submit">
                        <i class="fa fa-save"></i> {% if asaun == 'edit' %} Atualiza {% else %} Rejistu {% endif %}
                    </button>
                    <a class="btn btn-warning m-1" onclick="self.history.back()">
                        <span class="btn-label"><i class="fa fa-window-close"></i></span> Kansela
                    </a>
                </div>
            """)
        )




class BaseContentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ‑‑‑ Deskrisaun: usa CKEditor widget ‑‑‑
        self.fields['deskrisaun'].widget = CKEditorUploadingWidget(config_name='default')
        # (se la presiza upload iha editor, bele uza CKEditorWidget deit)

        # ‑‑‑ PDF: estiliza input file ‑‑‑
        self.fields['file_pdf'].widget.attrs.update({
            'class': 'form-control',
            'accept': 'application/pdf'
        })

        # Crispy Form Helper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'     # ✨ importante atu upload file
        self.helper.form_id = 'content-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'

        self.helper.layout = Layout(
            Row(
                Column('titlu', css_class='form-group col-md-12 mb-3'),
            ),
            Row(
                Column('lingua', css_class='form-group col-md-12 mb-3'),
            ),
            Row(
                Column('deskrisaun', css_class='form-group col-md-12 mb-3'),
            ),
            Row(                                               # ✨ linha foun ba PDF
                Column('file_pdf', css_class='form-group col-md-12 mb-3'),
            ),
            HTML("""
            <div class="form-group row mb-0">
                <div class="col-md-12 text-center">
                    <button type="submit" class="btn btn-labeled">
                        <i class="fa fa-save me-1"></i>
                        {% if asaun == 'edit' %}
                            {{ _("Atualiza") }}
                        {% else %}
                            {{ _("Rejistu") }}
                        {% endif %}
                    </button>
                    <button type="button" class="btn btn-labeled" onclick="window.history.back()">
                        <i class="fa fa-times me-1"></i>
                        {{ _("Kansela") }}
                    </button>
                </div>
            </div>

            """)
        )

    # Valida so PDF no limita tamainu (eksemp: 5 MB)
    def clean_file_pdf(self):
        pdf = self.cleaned_data.get('file_pdf')
        if pdf:
            if not pdf.name.lower().endswith('.pdf'):
                raise forms.ValidationError(_("Ami simu deit ficheru PDF."))
            if pdf.size > 5 * 1024 * 1024:
                raise forms.ValidationError(_("Taman maksimum: 5 MB."))
        return pdf

    class Meta:
        abstract = True
        model  = None            # será set ba form subclass
        fields = ['titlu', 'lingua', 'deskrisaun', 'file_pdf']
        labels = {
            'titlu':       _('Títulu'),
            'lingua':      _('Lingua'),
            'deskrisaun':  _('Deskrisaun'),
            'file_pdf':    _('Ficheiru PDF'),
        }


class FinansiamentunoapoiuForm(BaseContentForm):
    class Meta(BaseContentForm.Meta):
        model = Finansiamentunoapoiu


class PublikasaunkmboForm(BaseContentForm):
    class Meta(BaseContentForm.Meta):
        model = Publikasaunkmbo


class DokumentusimportantesForm(BaseContentForm):
    class Meta(BaseContentForm.Meta):
        model = Dokumentusimportantes

from .models import RegistuPartisipante
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, HTML

class RegistuPartisipanteForm(forms.ModelForm):
    class Meta:
        model = RegistuPartisipante
        fields = '__all__'
        exclude = ['data_rejistu', 'munucipio']
        widgets = {
            'naran': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'sexo': forms.Select(attrs={'class': 'form-control form-control-lg'}),
            'data_moris': forms.DateInput(attrs={'class': 'form-control form-control-lg', 'type': 'date'}),
            'postu': forms.Select(attrs={'class': 'form-control form-control-lg'}),
            'kategoria': forms.Select(attrs={'class': 'form-control form-control-lg'}),
            'pozisaun': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'naran_instituisaun': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Ex: exemplo@gmail.com'}),
            'suku': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'aldeia': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'no_eleitoral': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'fotografia': forms.ClearableFileInput(attrs={'class': 'form-control form-control-lg'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'partisipante_form'
        self.helper.form_class = 'needs-validation'
        self.helper.label_class = 'form-label fw-bold'
        self.helper.field_class = 'mb-4'

        self.helper.layout = Layout(
            Fieldset(
                'Favor Kompleta Formulariu Delegadu',
                Row(
                    Column('no_eleitoral', css_class='col-md-12'),
                    Column('fotografia', css_class='col-md-12'),
                    css_class='mb-4'
                ),
                Row(
                    Column('naran', css_class='col-md-12'),
                    Column('sexo', css_class='col-md-12'),
                    css_class='mb-4'
                ),
                Row(
                    Column('data_moris', css_class='col-md-12'),
                    css_class='mb-4'
                ),
                Row(
                    Column('postu', css_class='col-md-12'),
                    Column('kategoria', css_class='col-md-12'),
                    css_class='mb-4'
                ),
                Row(
                    Column('pozisaun', css_class='col-md-12'),
                    Column('naran_instituisaun', css_class='col-md-12'),
                    css_class='mb-4'
                ),
                Row(
                    Column('suku', css_class='col-md-12'),
                    Column('aldeia', css_class='col-md-12'),
                    css_class='mb-4'
                ),
                Row(
                    Column('telefone', css_class='col-md-12'),
                    Column('email', css_class='col-md-12'),
                    css_class='mb-4'
                ),
                css_class='border-bottom pb-3 mb-4'
            ),
            HTML("""
                <div class='d-flex justify-content-center gap-3 mt-4'>
                    <a class="btn btn-outline-secondary" onclick="window.history.back()">
                        <i class="fas fa-times me-2"></i> Kansela
                    </a>        
                    <button class="btn btn-primary" type="submit">
                        <i class="fas fa-save me-2"></i> 
                        {% if form.instance.pk %} Atualiza {% else %} Rejistu {% endif %}
                    </button>
                </div>
                """)
        )



class RegistuVoluntariuForm(forms.ModelForm):
    class Meta:
        model = RegistuVoluntariu
        fields = '__all__'
        exclude = ['data_rejistu', 'munucipio']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'voluntariu_form'

        # Ajusta widget de data
        self.fields['data_moris'].widget = forms.DateInput(attrs={'type': 'date'})

        self.helper.layout = Layout(
            Row(
                Column('naran', css_class='form-group col-md-6 mb-0'),
                Column('sexo', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('data_moris', css_class='form-group col-md-6 mb-0'),
                Column('pozisaun', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('postu', css_class='form-group col-md-6 mb-0'),
                Column('area_voluntariadu', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('lingua', css_class='form-group col-md-6 mb-0'),
                Column('telefone', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('email', css_class='form-group col-md-12 mb-0'),
            ),
            'deskrisaun',
            
            HTML("""
            <br>
            <div class='float-right'>
                <button class="btn btn-secondary m-1" type="submit">
                    <i class="fa fa-save"></i> 
                    {% if form.instance.pk %} Atualiza {% else %} Rejistu {% endif %}
                </button>
                <a class="btn btn-warning m-1" onclick="window.history.back()">
                    <i class="fa fa-window-close"></i> Kansela
                </a>        
            </div>
            """)
        )



class KontaktuamiForm(forms.ModelForm):
    class Meta:
        model = Kontaktuami
        fields = ['lokalizasaun', 'sukursal', 'website', 'email', 'numerutelemovel']


    def __init__(self, *args, **kwargs):
        super(KontaktuamiForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'kont_id'
        self.helper.layout = Layout(
            HTML("""
            <div class="container">
              <div class="row">
                <div class="col-md-6 form-group">
                  <input type="text" name="Lokalizasaun" class="form-control p-2" id="Lokalizasaun" placeholder="Lokalizasaun" required>
                </div>
                <div class="col-md-6 form-group mt-4 mt-md-0">
                  <input type="email" class="form-control p-2" name="email" id="email" placeholder="Email" required>
                </div>
              </div>
              <div class="form-group mt-4">
                <input type="number" class="form-control p-2" name="numerutelemovel" id="numerutelemovel" placeholder="No.Tlf" required>
              </div>
            </div>
            """),
            HTML("""
            <br>
            <div class='text-center'>
              <button id='kont_id' class="btn btn-secondary m-1" type="submit" style="background-color: rgb(4, 129, 245); margin-left: 15%;">
                <i class="fa fa-save"></i> Haruka Mensajen
              </button>
            </div>
            """)
        )


class ArtiguForm(forms.ModelForm):
    class Meta:
        model = Artigu
        fields = ['lingua', 'titlu', 'deskrisaun', 'file_pdf', 'data']
        widgets = {
            'data': DateInput(attrs={'type': 'date'})  # <-- ne'e mosu HTML5 date picker
        }

    def __init__(self, *args, **kwargs):
        super(ArtiguForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'artigu_form'
        self.helper.layout = Layout(
            Row(Column('lingua', css_class='form-group col-md-12 mb-0')),
            Row(Column('titlu', css_class='form-group col-md-12 mb-0')),
            Row(Column('deskrisaun', css_class='form-group col-md-12 mb-0')),
            Row(Column('file_pdf', css_class='form-group col-md-12 mb-0')),
            Row(Column('data', css_class='form-group col-md-12 mb-0')),
            HTML("""
                <br>
                <div class='float-right'>
                    <button id='artigu_submit' class="btn btn-secondary m-1" type="submit">
                        <i class="fa fa-save"></i> {% if asaun == 'edit' %} Atualiza {% else %} Rejistu {% endif %}
                    </button>
                    <a class="btn btn-warning m-1" onclick="self.history.back()">
                        <span class="btn-label"><i class="fa fa-window-close"></i></span> Kansela
                    </a>
                </div>
            """)
        )











# forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import RegistuMenbroKmbo
import re

class RegistuMenbroKmboModelForm(forms.ModelForm):
    # Aumenta kampu temporariu atu hetan naran anterior (ba update)
    naran_anterior = forms.CharField(required=False, widget=forms.HiddenInput())
    
    class Meta:
        model = RegistuMenbroKmbo
        fields = '__all__'
        widgets = {
            'naran_kompletu': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Hatama naran kompletu'
            }),
            'nomor_eleitoral_bi': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Hatama nomor eleitoral ka BI'
            }),
            'idade': forms.Select(attrs={
                'class': 'form-control'
            }),
            'generu': forms.Select(attrs={
                'class': 'form-control'
            }),
            'hela_fatin_atual': forms.Select(attrs={
                'class': 'form-control'
            }),
            'posto': forms.Select(attrs={
                'class': 'form-control'
            }),
            'habilitasaun_literaria': forms.Select(attrs={
                'class': 'form-control'
            }),
            'servisu_hanesan': forms.Select(attrs={
                'class': 'form-control'
            }),
            'fatin_servisu': forms.Select(attrs={
                'class': 'form-control'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Hatama numeru telefone'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Hatama email'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        # Guarda instância atual ba validação
        self.instance_atual = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        
        # Hadia label ho klaru
        self.fields['naran_kompletu'].label = "Naran Kompletu *"
        self.fields['idade'].label = "Idade *"
        self.fields['generu'].label = "Jéneru *"
        self.fields['nomor_eleitoral_bi'].label = "Nomor Eleitoral ka BI *"
        self.fields['hela_fatin_atual'].label = "Hela Fatin Atual *"
        self.fields['posto'].label = "Postu *"
        self.fields['habilitasaun_literaria'].label = "Habilitasaun Literária *"
        self.fields['servisu_hanesan'].label = "Servisu hanesan *"
        self.fields['fatin_servisu'].label = "Fatin Servisu *"
        self.fields['telefone'].label = "Telefone"
        self.fields['email'].label = "Email"
        
        # Garante katak field hotu iha class 'form-control'
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect, forms.HiddenInput)):
                if 'class' not in field.widget.attrs:
                    field.widget.attrs['class'] = 'form-control'
                if field.required and field_name != 'naran_anterior':
                    field.widget.attrs['required'] = 'required'
        
        # Se update, guarda naran anterior
        if self.instance_atual and self.instance_atual.pk:
            self.initial['naran_anterior'] = self.instance_atual.naran_kompletu
    
    def clean_nomor_eleitoral_bi(self):
        nomor = self.cleaned_data.get('nomor_eleitoral_bi')
        
        if not nomor:
            raise ValidationError("Nomor Eleitoral ka BI tenke prense!")
        
        # Hili espasu branku
        nomor = nomor.strip().upper()
        
        # Determina tipu dokumentu
        if nomor.isdigit():
            tipu = 'ELEITORAL'
            # Valida formatu Eleitoral (exemplu: 8-12 numeru)
            if len(nomor) < 8 or len(nomor) > 12:
                raise ValidationError("Nomor Eleitoral tenke iha entre 8-12 numeru!")
        else:
            tipu = 'BI'
            # Valida formatu BI (padraun Timor nian: Letra+Numeru, 6-15 karakter)
            if not re.match(r'^[A-Z0-9]{6,15}$', nomor):
                raise ValidationError("""
                    Formatu BI la validu! 
                    - Tenke iha entre 6-15 karakter
                    - Letra boot hotu (A-Z) no numeru (0-9)
                    - Exemplo: A123456, TL123456
                """)
        
        # Verifika duplikasaun (ba input foun ka update)
        if self.instance_atual and self.instance_atual.pk:
            # Kasu update: permite nia nia dokumentu rasik
            if self.instance_atual.nomor_eleitoral_bi == nomor:
                return nomor
        
        # Verifika dokumentu ne'ebé hanesan iha database
        duplicatas = RegistuMenbroKmbo.objects.filter(
            nomor_eleitoral_bi=nomor
        )
        
        if duplicatas.exists():
            membro_existente = duplicatas.first()
            
            # Kria mensajem ho formatu bonitu
            mensagem = "╔════════════════════════════════════╗\n"
            mensagem += "║       DUPLIKASAUN DETEKTADU       ║\n"
            mensagem += "╚════════════════════════════════════╝\n\n"
            mensagem += f"❌ Númeru {tipu} '{nomor}' rejista ona!\n\n"
            mensagem += f"📋 Detallu Rejistu Existente:\n"
            mensagem += f"   👤 Naran: {membro_existente.naran_kompletu}\n"
            mensagem += f"   📅 Data Rejistu: {membro_existente.data_rejistu.strftime('%d/%m/%Y %H:%M')}\n"
            mensagem += f"   🏠 Hela Fatin: {membro_existente.get_hela_fatin_atual_display()}\n"
            mensagem += f"   📄 Tipu: {tipu}\n\n"
            
            # Verifika karik nia rejista uluk ho dokumentu seluk
            if tipu == 'BI':
                # Buka karik iha rejistu ho eleitoral ho naran hanesan
                eleitoral_possivel = RegistuMenbroKmbo.objects.filter(
                    Q(naran_kompletu__icontains=membro_existente.naran_kompletu) & 
                    Q(tipu_dokumentu='ELEITORAL')
                ).exclude(id=membro_existente.id).first()
                
                if eleitoral_possivel:
                    mensagem += "⚠️  ATENSAUN ESPESIAL!\n"
                    mensagem += "   Ema ne'e mós iha rejistu ho Kartaun Eleitoral:\n"
                    mensagem += f"   👤 Naran: {eleitoral_possivel.naran_kompletu}\n"
                    mensagem += f"   📅 Data: {eleitoral_possivel.data_rejistu.strftime('%d/%m/%Y')}\n"
                    mensagem += "   ❗ Keta rejista dala rua ho dokumentu diferente!\n\n"
            
            mensagem += "✅ Solusaun:\n"
            mensagem += "   1. Uza rejistu existente (buka iha lista)\n"
            mensagem += "   2. Se ne'e ema diferente, verifika numeru dokumentu\n"
            
            raise ValidationError(mensagem)
        
        return nomor
    
    def clean(self):
        cleaned_data = super().clean()
        nomor = cleaned_data.get('nomor_eleitoral_bi')
        naran_kompletu = cleaned_data.get('naran_kompletu')
        naran_anterior = cleaned_data.get('naran_anterior')
        
        if not nomor or not naran_kompletu:
            return cleaned_data
        
        # Validasaun komplementar: verifika karik ema uja BI maibe rejista uluk ho eleitoral
        if not nomor.isdigit():  # BI
            # Buka rejistu ho eleitoral ho naran ne'ebé hanesan
            naran_normal = ' '.join(naran_kompletu.strip().lower().split())
            
            # Se update, esklui nia rasik
            query = RegistuMenbroKmbo.objects.filter(
                tipu_dokumentu='ELEITORAL'
            )
            
            if self.instance_atual and self.instance_atual.pk:
                query = query.exclude(pk=self.instance_atual.pk)
            
            # Verifika naran ne'ebé hanesan ho dokumentu eleitoral
            for membro in query:
                membro_naran = ' '.join(membro.naran_kompletu.strip().lower().split())
                # Verifika similaridade naran
                if membro_naran == naran_normal or naran_normal in membro_naran or membro_naran in naran_normal:
                    # Verifika se ita muda husi eleitoral ba BI
                    if naran_anterior and ' '.join(naran_anterior.strip().lower().split()) == membro_naran:
                        # Ita update husi eleitoral ba BI - permited
                        continue
                    
                    # Verifika se ita uja BI maibe iha rejistu eleitoral ho naran hanesan
                    if not self.instance_atual or self.instance_atual.pk != membro.pk:
                        mensagem_aviso = f"""
╔══════════════════════════════════════════════════════════╗
║              REJISTU KRUZADA DETEKTADU                  ║
╚══════════════════════════════════════════════════════════╝

⚠️  AVISO IMPORTANTE!

Ita koko atu rejista ho BILHETE IDENTIDADE (BI), 
maibé sistema hetan rejistu uluk ho KARTAUN ELEITORAL:

┌────────────────────────────────────────────────┐
│ DADUS REJISTU ELEITORAL                        │
├────────────────────────────────────────────────┤
│ 👤 Naran: {membro.naran_kompletu[:30]}
│ 📅 Data: {membro.data_rejistu.strftime('%d/%m/%Y')}
│ 🏠 Hela Fatin: {membro.get_hela_fatin_atual_display()}
│ 📄 Dokumentu: Kartaun Eleitoral
│ 🔢 Númeru: {membro.nomor_eleitoral_bi}
└────────────────────────────────────────────────┘

❓ PERGUNTA:
   Ema ne'e ema ida deit ka ema diferente?

📋 INSTRUSAUN:
   ✓ SE EMA IDA DEIT: 
     > Keta rejista fali! Uza rejistu existente
     > Buka nia naran iha lista membro
     > Atualiza dadus se presiza (mudansa BI)
   
   ✓ SE EMA DIFERENTE: 
     > Kontinua ho rejistu foun

     
     






     > Verifika numeru BI ho di'ak
     > Asegura numeru dokumentu la sala
"""
                        
                        # Aumenta mensajen ba form
                        self.add_error('nomor_eleitoral_bi', mensagem_aviso)
                        break
        
        return cleaned_data