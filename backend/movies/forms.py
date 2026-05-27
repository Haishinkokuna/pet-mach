"""
Forms for Pet Match application
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Pets, Breeds


class LoginForm(AuthenticationForm):
    """Formulario de autenticación personalizado"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Usuario'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
    )


class PetsForm(forms.ModelForm):
    """Formulario para crear y editar mascotas"""
    class Meta:
        model = Pets
        fields = ['breed', 'name', 'gender', 'birth_date', 'description', 'image', 'health_certificate', 'is_available']
        widgets = {
            'breed': forms.Select(attrs={
                'class': 'form-control'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la mascota'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control'
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Información de salud, genética y cualidades de reproducción'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'health_certificate': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'breed': 'Raza',
            'name': 'Nombre',
            'gender': 'Sexo',
            'birth_date': 'Fecha de Nacimiento',
            'description': 'Descripción (Salud/Genética)',
            'image': 'Foto de la Mascota',
            'health_certificate': 'Certificado de Salud',
            'is_available': 'Disponible para cruza',
        }

    def clean_image(self):
        """Validar tamaño de imagen"""
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB
                raise forms.ValidationError('La imagen no puede exceder 5MB')
        return image


class BreedsForm(forms.ModelForm):
    """Formulario para crear y editar razas"""
    class Meta:
        model = Breeds
        fields = ['name', 'description', 'characteristics']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la raza'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción general'
            }),
            'characteristics': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Características principales'
            }),
        }
        labels = {
            'name': 'Nombre de la Raza',
            'description': 'Descripción',
            'characteristics': 'Características',
        }
