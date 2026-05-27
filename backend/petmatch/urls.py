"""
URL Configuration for petmatch project.
"""
from django.conf import settings
from django.urls import include, re_path, path
from django.contrib import admin

from movies.api import get_pets, get_my_pets, delete_pet, login_api

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^', include('movies.urls')),
    
    # Rutas para la API de Flutter
    path('api/login/', login_api, name='api_login'),
    path('api/mascotas/', get_pets, name='api_pets'),
    path('api/mis-mascotas/', get_my_pets, name='api_my_pets'),
    path('api/mascotas/<int:pk>/', delete_pet, name='api_delete_pet'),
]

# Serve media files during development
if settings.DEBUG:
    from django.views.static import serve
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
