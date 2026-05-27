"""
URL Configuration for movies app (Pet Match)
"""
from django.urls import re_path
from . import views

urlpatterns = [
    # Autenticación
    re_path(r'^login/$', views.login_view, name='login'),
    re_path(r'^logout/$', views.logout_view, name='logout'),
    re_path(r'^register/$', views.register_view, name='register'),

    # Página de inicio
    re_path(r'^$', views.index, name='index'),

    # Mascotas - CRUD
    re_path(r'^mascotas/$', views.pet_list, name='pet_list'),
    re_path(r'^mis-mascotas/$', views.my_pets, name='my_pets'),
    re_path(r'^mascota/(?P<pk>\d+)/$', views.pet_detail, name='pet_detail'),
    re_path(r'^mascota/crear/$', views.pet_create, name='pet_create'),
    re_path(r'^mascota/(?P<pk>\d+)/editar/$', views.pet_edit, name='pet_edit'),
    re_path(r'^mascota/(?P<pk>\d+)/eliminar/$', views.pet_delete, name='pet_delete'),
]
