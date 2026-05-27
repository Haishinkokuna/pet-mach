"""
Views for Pet Match application
Vistas basadas en funciones (FBV) para CRUD de mascotas
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import Http404
from django.views.decorators.http import require_http_methods
from .models import Pets, Breeds
from .forms import PetsForm, LoginForm, BreedsForm


# ============================================================================
# VISTAS DE AUTENTICACIÓN
# ============================================================================

def login_view(request):
    """Vista para login de usuarios"""
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('pet_list')
    else:
        form = LoginForm()
    
    context = {
        'form': form,
        'title': 'Iniciar Sesión - Pet Match'
    }
    return render(request, 'movies/login.html', context)


def logout_view(request):
    """Vista para logout de usuarios"""
    logout(request)
    return redirect('login')


def register_view(request):
    """Vista para registro de nuevos usuarios"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            context = {
                'error': 'Las contraseñas no coinciden',
                'title': 'Registro - Pet Match'
            }
            return render(request, 'movies/register.html', context)

        if User.objects.filter(username=username).exists():
            context = {
                'error': 'El usuario ya existe',
                'title': 'Registro - Pet Match'
            }
            return render(request, 'movies/register.html', context)

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            login(request, user)
            return redirect('pet_list')
        except Exception as e:
            context = {
                'error': f'Error al registrar: {str(e)}',
                'title': 'Registro - Pet Match'
            }
            return render(request, 'movies/register.html', context)
    
    context = {
        'title': 'Registro - Pet Match'
    }
    return render(request, 'movies/register.html', context)


# ============================================================================
# VISTAS CRUD DE MASCOTAS
# ============================================================================

def pet_list(request):
    """Listar todas las mascotas (pública)"""
    pets = Pets.objects.select_related('owner', 'breed').filter(is_available=True)
    
    # Filtro por raza
    breed_id = request.GET.get('breed')
    if breed_id:
        pets = pets.filter(breed_id=breed_id)
    
    # Búsqueda por nombre
    search = request.GET.get('search')
    if search:
        pets = pets.filter(name__icontains=search)
    
    breeds = Breeds.objects.all()
    
    context = {
        'pets': pets,
        'breeds': breeds,
        'title': 'Mascotas Disponibles - Pet Match',
        'search': search,
    }
    return render(request, 'movies/pet_list.html', context)


def my_pets(request):
    """Listar las mascotas del usuario autenticado"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    pets = Pets.objects.filter(owner=request.user).select_related('breed')
    
    context = {
        'pets': pets,
        'title': 'Mis Mascotas - Pet Match',
        'my_pets': True
    }
    return render(request, 'movies/pet_list.html', context)


def pet_detail(request, pk):
    """Ver detalle de una mascota"""
    pet = get_object_or_404(Pets, pk=pk)
    
    context = {
        'pet': pet,
        'title': f'{pet.name} - Pet Match',
    }
    return render(request, 'movies/pet_detail.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def pet_create(request):
    """Crear una nueva mascota - Requiere autenticación"""
    if request.method == 'POST':
        form = PetsForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            return redirect('pet_detail', pk=pet.pk)
    else:
        form = PetsForm()
    
    context = {
        'form': form,
        'title': 'Agregar Nueva Mascota - Pet Match',
        'action': 'Crear'
    }
    return render(request, 'movies/pet_form.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def pet_edit(request, pk):
    """Editar una mascota - Requiere autenticación"""
    pet = get_object_or_404(Pets, pk=pk)
    
    # Verificar que el usuario sea el dueño
    if pet.owner != request.user:
        return redirect('my_pets')
    
    if request.method == 'POST':
        form = PetsForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('pet_detail', pk=pet.pk)
    else:
        form = PetsForm(instance=pet)
    
    context = {
        'form': form,
        'pet': pet,
        'title': f'Editar {pet.name} - Pet Match',
        'action': 'Editar'
    }
    return render(request, 'movies/pet_form.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def pet_delete(request, pk):
    """Eliminar una mascota - Requiere autenticación"""
    pet = get_object_or_404(Pets, pk=pk)
    
    # Verificar que el usuario sea el dueño
    if pet.owner != request.user:
        return redirect('my_pets')
    
    if request.method == 'POST':
        pet.delete()
        return redirect('my_pets')
    
    context = {
        'pet': pet,
        'title': f'Eliminar {pet.name} - Pet Match'
    }
    return render(request, 'movies/pet_confirm_delete.html', context)


# ============================================================================
# VISTAS DE PÁGINA DE INICIO
# ============================================================================

def index(request):
    """Página de inicio"""
    total_pets = Pets.objects.filter(is_available=True).count()
    total_breeds = Breeds.objects.count()
    recent_pets = Pets.objects.filter(is_available=True).select_related(
        'breed', 'owner'
    )[:6]
    
    context = {
        'total_pets': total_pets,
        'total_breeds': total_breeds,
        'recent_pets': recent_pets,
        'title': 'Pet Match - Plataforma de Cruza Responsable'
    }
    return render(request, 'movies/index.html', context)
