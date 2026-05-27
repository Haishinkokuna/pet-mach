#!/usr/bin/env python
"""
Script para cargar datos de prueba en Pet Match
Uso: python manage.py shell < load_test_data.py
"""

from django.contrib.auth.models import User
from movies.models import Breeds, Pets
from datetime import date

# Crear usuarios de prueba
print("🔧 Creando usuarios de prueba...")
try:
    user1 = User.objects.get(username='dueno1')
except User.DoesNotExist:
    user1 = User.objects.create_user(
        username='dueno1',
        email='dueno1@petmatch.com',
        password='password123',
        first_name='Juan',
        last_name='García'
    )
    print(f"✓ Usuario creado: {user1.username}")

try:
    user2 = User.objects.get(username='dueno2')
except User.DoesNotExist:
    user2 = User.objects.create_user(
        username='dueno2',
        email='dueno2@petmatch.com',
        password='password123',
        first_name='María',
        last_name='López'
    )
    print(f"✓ Usuario creado: {user2.username}")

# Crear razas
print("\n🐕 Creando razas...")

razas_data = [
    {
        'name': 'Labrador Retriever',
        'description': 'Perro de raza grande, amigable y leal, excelente para familias',
        'characteristics': 'Grande, energético, buen nadador, inteligente, 55-80 lbs'
    },
    {
        'name': 'Pastor Alemán',
        'description': 'Perro inteligente y versátil, excelente para trabajo',
        'characteristics': 'Grande, leal, entrenador, 50-90 lbs, activo'
    },
    {
        'name': 'Golden Retriever',
        'description': 'Perro hermoso y amigable, excelente temperamento',
        'characteristics': 'Grande, dorando, inteligente, 55-75 lbs, amigable'
    },
    {
        'name': 'Bulldog Francés',
        'description': 'Perro pequeño, compacto y musculoso',
        'characteristics': 'Pequeño, 22-28 lbs, robusto, buen compañero'
    },
    {
        'name': 'Beagle',
        'description': 'Perro pequeño de caza, excelente olfato',
        'characteristics': 'Pequeño, 20-30 lbs, energético, buscador'
    },
    {
        'name': 'Cocker Spaniel',
        'description': 'Perro mediano cariñoso y obediente',
        'characteristics': 'Mediano, 25-30 lbs, activo, compañero leal'
    }
]

razas = {}
for raza_data in razas_data:
    raza, created = Breeds.objects.get_or_create(
        name=raza_data['name'],
        defaults={
            'description': raza_data['description'],
            'characteristics': raza_data['characteristics']
        }
    )
    razas[raza_data['name']] = raza
    if created:
        print(f"✓ Raza creada: {raza.name}")
    else:
        print(f"✓ Raza ya existe: {raza.name}")

# Crear mascotas de prueba
print("\n🐾 Creando mascotas de prueba...")

mascotas_data = [
    {
        'owner': user1,
        'breed': razas['Labrador Retriever'],
        'name': 'Max',
        'gender': 'M',
        'birth_date': date(2020, 5, 15),
        'description': 'Max es un Labrador saludable con excelente temperamento. Línea genética comprobada, apto para reproducción. Vacunas al día, certificado veterinario disponible.',
        'is_available': True
    },
    {
        'owner': user1,
        'breed': razas['Labrador Retriever'],
        'name': 'Luna',
        'gender': 'F',
        'birth_date': date(2019, 8, 22),
        'description': 'Luna es una Labrador de 5 años, saludable y con buen temperamento. Excelentes características para reproducción. Documentos veterinarios completos.',
        'is_available': True
    },
    {
        'owner': user2,
        'breed': razas['Pastor Alemán'],
        'name': 'Rex',
        'gender': 'M',
        'birth_date': date(2021, 2, 10),
        'description': 'Rex es un Pastor Alemán joven, musculoso y de buen temperamento. Entrenado básicamente, apto para reproducción futura.',
        'is_available': False
    },
    {
        'owner': user2,
        'breed': razas['Golden Retriever'],
        'name': 'Bella',
        'gender': 'F',
        'birth_date': date(2020, 11, 5),
        'description': 'Bella es una Golden Retriever hermosa con pelaje dorado intenso. Temperamento excelente, documentación veterinaria completa. Disponible para cruza responsable.',
        'is_available': True
    },
    {
        'owner': user1,
        'breed': razas['Bulldog Francés'],
        'name': 'Paco',
        'gender': 'M',
        'birth_date': date(2021, 7, 20),
        'description': 'Paco es un Bulldog Francés compacto y musculoso. Excelentes características de raza, salud comprobada. Ideal para reproducción selectiva.',
        'is_available': True
    },
    {
        'owner': user2,
        'breed': razas['Beagle'],
        'name': 'Charlie',
        'gender': 'M',
        'birth_date': date(2019, 3, 15),
        'description': 'Charlie es un Beagle adulto de 5 años, activo y saludable. Excelente olfato y energía. Documentación veterinaria al día.',
        'is_available': True
    }
]

for mascota_data in mascotas_data:
    mascota, created = Pets.objects.get_or_create(
        name=mascota_data['name'],
        owner=mascota_data['owner'],
        defaults={
            'breed': mascota_data['breed'],
            'gender': mascota_data['gender'],
            'birth_date': mascota_data['birth_date'],
            'description': mascota_data['description'],
            'is_available': mascota_data['is_available']
        }
    )
    if created:
        print(f"✓ Mascota creada: {mascota.name} ({mascota.breed.name}) - {mascota.owner.first_name}")
    else:
        print(f"✓ Mascota ya existe: {mascota.name}")

print("\n" + "="*60)
print("✨ Datos de prueba cargados correctamente!")
print("="*60)

# Mostrar estadísticas
print(f"\nEstadísticas:")
print(f"- Usuarios: {User.objects.count()}")
print(f"- Razas: {Breeds.objects.count()}")
print(f"- Mascotas: {Pets.objects.count()}")
print(f"- Mascotas disponibles: {Pets.objects.filter(is_available=True).count()}")

print("\nAcceso:")
print("- Usuario: dueno1 / Contraseña: password123")
print("- Usuario: dueno2 / Contraseña: password123")
print("\n¡Listo! Ahora puedes iniciar sesión en http://localhost:8000/login/")
