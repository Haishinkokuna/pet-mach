"""
Models for Pet Match - CRUD de mascotas para gestión de cruza responsable
"""
from django.db import models
from django.contrib.auth.models import User


class Breeds(models.Model):
    """Modelo de Razas de mascotas"""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nombre de la Raza'
    )
    description = models.TextField(
        verbose_name='Descripción',
        help_text='Descripción general de la raza'
    )
    characteristics = models.TextField(
        verbose_name='Características',
        help_text='Características principales de la raza',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Raza'
        verbose_name_plural = 'Razas'
        ordering = ['name']

    def __str__(self):
        return self.name


class Pets(models.Model):
    """Modelo de Mascotas para Pet Match"""
    GENDER_CHOICES = (
        ('M', 'Macho'),
        ('F', 'Hembra'),
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Dueño'
    )
    breed = models.ForeignKey(
        Breeds,
        on_delete=models.PROTECT,
        verbose_name='Raza'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Nombre'
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name='Sexo'
    )
    birth_date = models.DateField(
        verbose_name='Fecha de Nacimiento'
    )
    description = models.TextField(
        verbose_name='Descripción de Salud/Genética',
        help_text='Información sobre salud, historial genético y cualidades de reproducción'
    )
    image = models.ImageField(
        upload_to='pets/',
        verbose_name='Foto',
        help_text='Foto del animal'
    )
    health_certificate = models.FileField(
        upload_to='certificates/',
        verbose_name='Certificado de Salud',
        blank=True,
        null=True
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name='Disponible para cruza'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Mascota'
        verbose_name_plural = 'Mascotas'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.breed.name})"

    def age(self):
        """Calcula la edad de la mascota"""
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )
