# 🐾 Pet Match App

Una aplicación multiplataforma para gestión responsable de cruza de mascotas. Permite a los dueños de mascotas conectarse y encontrar parejas ideales para sus animales, basándose en raza, salud y genética.

## 📋 Descripción

**Pet Match** es una aplicación completa (full-stack) que facilita:

- 👥 Registro y autenticación de usuarios
- 🐕 Gestión de perfiles de mascotas con información de salud y genética
- 🔍 Búsqueda y filtrado de mascotas disponibles para cruza
- 📊 Seguimiento de razas y características de animales
- 📁 Gestión de certificados de salud

## 🏗️ Arquitectura del Proyecto

```
pet_match_app/
├── lib/                           # Frontend Flutter
│   └── main.dart                  # Aplicación principal con UI
├── backend/                       # Backend Django REST API
│   ├── petmatch/                  # Configuración del proyecto Django
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── movies/                    # App principal de Django (gestión de mascotas)
│   │   ├── models.py              # Modelos: Pets, Breeds
│   │   ├── api.py                 # Endpoints REST
│   │   ├── views.py
│   │   └── urls.py
│   ├── requirements.txt           # Dependencias Python
│   ├── manage.py
│   └── db.sqlite3                 # Base de datos (local)
├── android/                       # Configuración Android
├── ios/                           # Configuración iOS
├── web/                           # Configuración Web
├── windows/, linux/, macos/       # Configuraciones de otros sistemas
└── pubspec.yaml                   # Dependencias Flutter
```

## 🛠️ Stack Tecnológico

### Frontend
- **Flutter 3.11.5+** - Framework multiplataforma
- **Dart** - Lenguaje de programación
- **HTTP** - Cliente HTTP para peticiones a la API

### Backend
- **Django 4.2** - Framework web Python
- **Django REST API** - Endpoints REST
- **SQLite** - Base de datos local
- **Pillow** - Manejo de imágenes

## ⚙️ Configuración Local

### Requisitos Previos
- Flutter 3.11.5 o superior
- Python 3.8 o superior
- pip (gestor de paquetes Python)

### Backend (Django)

1. **Navega a la carpeta del backend:**
```bash
cd backend
```

2. **Crea un entorno virtual:**
```bash
python -m venv venv
```

3. **Activa el entorno virtual:**
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. **Instala las dependencias:**
```bash
pip install -r requirements.txt
```

5. **Ejecuta las migraciones:**
```bash
python manage.py migrate
```

6. **Crea un superusuario (opcional, para acceder al admin):**
```bash
python manage.py createsuperuser
```

7. **Inicia el servidor de desarrollo:**
```bash
python manage.py runserver
```

El API estará disponible en: `http://127.0.0.1:8000/api`

### Frontend (Flutter)

1. **En la raíz del proyecto, obtén las dependencias:**
```bash
flutter pub get
```

2. **Ejecuta la aplicación:**

**En emulador Android:**
```bash
flutter run
```

**En navegador (web):**
```bash
flutter run -d chrome
```

**En dispositivo iOS:**
```bash
flutter run -d ios
```

## 🔌 API Endpoints

### Mascotas
- `GET /api/pets/` - Obtiene todas las mascotas disponibles
- `POST /api/pets/` - Crea una nueva mascota
- `DELETE /api/pets/<id>/` - Elimina una mascota
- `GET /api/my-pets/` - Obtiene las mascotas del usuario

### Autenticación
- `POST /api/login/` - Login de usuario (mock)

## 📦 Modelos de Base de Datos

### Breeds (Razas)
```
- id (PK)
- name (str, único)
- description (texto)
- characteristics (texto)
- created_at (timestamp)
- updated_at (timestamp)
```

### Pets (Mascotas)
```
- id (PK)
- owner (FK → User)
- breed (FK → Breeds)
- name (str)
- gender (M/F)
- birth_date (date)
- description (texto - salud/genética)
- image (ImageField)
- health_certificate (FileField, opcional)
- is_available (boolean)
```

## 🚀 Deployment

### Frontend (Vercel)
La aplicación Flutter está desplegada en Vercel. Para actualizar:
```bash
flutter build web
# Sube los archivos de build/web a Vercel
```

### Backend (PythonAnywhere)
Para desplegar en PythonAnywhere:
1. Sube este repositorio a GitHub
2. En PythonAnywhere, clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/pet-match.git
   ```
3. Configura el entorno virtual con `requirements.txt`
4. Apunta el WSGI a `backend/petmatch/wsgi.py`
5. Configura las variables de entorno necesarias

**Variables de entorno importantes para producción:**
```
DEBUG=False
ALLOWED_HOSTS=tu-dominio.pythonanywhere.com
SECRET_KEY=tu-clave-secreta
```

## 📝 Estructura de Archivos Importante

| Archivo | Descripción |
|---------|------------|
| `lib/main.dart` | Punto de entrada de la aplicación Flutter |
| `backend/petmatch/settings.py` | Configuración de Django |
| `backend/movies/models.py` | Definición de modelos (Pets, Breeds) |
| `backend/movies/api.py` | Endpoints REST |
| `pubspec.yaml` | Dependencias de Flutter |
| `backend/requirements.txt` | Dependencias de Python |

## 🔐 Notas de Seguridad

- ⚠️ En producción, cambia la `SECRET_KEY` en `backend/petmatch/settings.py`
- ⚠️ Configura `DEBUG = False` en producción
- ⚠️ Usa CORS headers apropiados para la comunicación frontend-backend
- ⚠️ Implementa autenticación real (JWT, Token Auth) en lugar del mock actual

## 👨‍💻 Desarrollo

### Flujo de trabajo recomendado:

1. **Backend:**
   ```bash
   cd backend
   source venv/bin/activate  # o venv\Scripts\activate en Windows
   python manage.py runserver
   ```

2. **Frontend (en otra terminal):**
   ```bash
   flutter run
   ```

### Crear datos de prueba:

Usa el script incluido:
```bash
cd backend
python load_test_data.py
```

## 🐛 Troubleshooting

**Error de conexión con la API:**
- Verifica que el servidor Django está corriendo en `http://127.0.0.1:8000`
- Revisa que el `baseUrl` en `lib/main.dart` coincide con tu URL de API

**Error al hacer login:**
- Actualmente el login es mock para permitir desarrollo sin servidor
- En producción, implementa autenticación real con JWT

**Imágenes de mascotas no se muestran:**
- Asegúrate que Django está sirviendo archivos estáticos (`DEBUG = True` en desarrollo)
- En producción, configura AWS S3 o similar para almacenamiento de archivos

## 📚 Referencias

- [Flutter Documentation](https://flutter.dev/docs)
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PythonAnywhere Docs](https://help.pythonanywhere.com/)
- [Vercel Documentation](https://vercel.com/docs)

## 📄 Licencia

Este proyecto está bajo licencia MIT. Puedes usarlo libremente para fines educativos y comerciales.

## 👤 Autor

Desarrollado como proyecto académico en UNAB - Semana 11 del curso de Desarrollo Web.

---

**¿Preguntas?** Revisa los archivos de configuración o abre un issue en el repositorio de GitHub.
