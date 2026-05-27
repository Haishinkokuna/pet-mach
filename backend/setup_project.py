"""
Script para inicializar el proyecto Pet Match
Ejecutar: python setup_project.py
"""

import os
import sys
from django.core.management import execute_from_command_line


def main():
    """Inicializa el proyecto Django"""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "petmatch.settings")
    
    print("=" * 60)
    print("🐾 Pet Match - Inicializador del Proyecto")
    print("=" * 60)
    
    print("\n1. Ejecutando migraciones...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migraciones completadas\n")
    except Exception as e:
        print(f"❌ Error en migraciones: {e}\n")
        return False
    
    print("2. Recopilando archivos estáticos...")
    try:
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        print("✅ Archivos estáticos recopilados\n")
    except Exception as e:
        print(f"⚠️  Advertencia en colecta de estáticos: {e}\n")
    
    print("=" * 60)
    print("✨ Proyecto inicializado correctamente!")
    print("=" * 60)
    print("\nPasos siguientes:")
    print("1. Crear superusuario: python manage.py createsuperuser")
    print("2. Ejecutar servidor: python manage.py runserver")
    print("3. Abrir navegador: http://localhost:8000")
    print("\nAdmin: http://localhost:8000/admin")
    print("=" * 60)
    
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
