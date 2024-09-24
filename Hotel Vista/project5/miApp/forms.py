from django.forms import ModelForm
from .models import informe
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserChangeForm


class informeForm(ModelForm):
    class Meta:
        model = informe
        fields = ['title', 'description', 'important']



class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(required=False)  #campo opcional, 

    class Meta:
        model = User
        fields = ('email',)


class ChangePasswordForm(forms.Form):
    new_password1 = forms.CharField(label='Nueva contraseña', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 != new_password2:
            raise forms.ValidationError("Las contraseñas no coinciden. Por favor, inténtalo de nuevo.")