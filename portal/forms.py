from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, HTML
from .models import Rejistu  # Importa modelo ne'e

class RejistuForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False  # Password hetan durante registu
    )
    password2 = forms.CharField(
        label=_("Confirm Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Rejistu
        fields = ['naran', 'email', 'kontaktu', 'pozisaun', 'fotografia']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get user from kwargs
        super(RejistuForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'rejistu_id'

        # Define se ita iha update ka registu
        if self.instance.pk:  # Update mode (instance exists)
            self.fields.pop('password1', None)
            self.fields.pop('password2', None)

        # Add group_name field only for admin users
        if user and user.groups.filter(name='admin').exists():
            self.fields['group_name'] = forms.ChoiceField(
                choices=[('admin', 'Admin'), ('editor', 'Editor'), ('ekipa', 'Ekipa')],
                required=True
            )
        
        self.helper.layout = Layout(
            Row(
                Column(Field('naran', css_class='form-group col-md-12 mb-0')),
                Column(Field('email', css_class='form-group col-md-12 mb-0')),
            ),
            Row(
                Column(Field('kontaktu', css_class='form-group col-md-12 mb-0')),
                Column(Field('pozisaun', css_class='form-group col-md-12 mb-0')),
            ),
            Column(Field('fotografia', css_class='form-group col-md-12 mb-0')),
            HTML("<br>"),
            Column(Field('group_name', css_class='form-group col-md-12 mb-0') if user and user.groups.filter(name='admin').exists() else None),  # Conditional field
            Row(
                Column(Field('password1', css_class='form-group col-md-12 mb-0')),
                Column(Field('password2', css_class='form-group col-md-12 mb-0')),
            ),
            HTML("""
                <div class="col-sm-12 text-center" style="float:right">
                    <button type="submit" class="btn btn-info btn-xs"><i class="fa fa-save"></i> Submete</button>
                    <button type="button" class="btn btn-danger btn-xs" onclick="window.history.back();"><i class="fa fa-close"></i> Kansela</button>
                </div>
            """),
        )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if not self.instance.pk:  # Only check passwords if in registration mode
            if password1 and password2:
                if password1 != password2:
                    raise forms.ValidationError(_("Passwords do not match."), code='password_mismatch')

                password_validation.validate_password(password1)
        
        return cleaned_data


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True, 'id': 'old_password', 'class': 'form-control'}),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'id': 'new_password', 'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Confirm new password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'id': 'confirm_password', 'class': 'form-control'}),
    )
