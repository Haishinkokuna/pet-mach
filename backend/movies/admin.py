from django.contrib import admin
from .models import Pets, Breeds


@admin.register(Breeds)
class BreedsAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    fieldsets = (
        ('Información General', {
            'fields': ('name', 'description', 'characteristics')
        }),
    )


@admin.register(Pets)
class PetsAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed', 'owner', 'gender', 'birth_date', 'is_available', 'created_at')
    search_fields = ('name', 'owner__username', 'breed__name')
    list_filter = ('breed', 'gender', 'is_available', 'created_at')
    readonly_fields = ('created_at', 'updated_at', 'age')
    fieldsets = (
        ('Información de la Mascota', {
            'fields': ('name', 'breed', 'owner', 'gender', 'birth_date')
        }),
        ('Salud y Genética', {
            'fields': ('description', 'health_certificate')
        }),
        ('Disponibilidad', {
            'fields': ('is_available',)
        }),
        ('Multimedia', {
            'fields': ('image',)
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at', 'age'),
            'classes': ('collapse',)
        }),
    )

    def age(self, obj):
        return f"{obj.age()} años"
    age.short_description = 'Edad'
