from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Pets
import json

@csrf_exempt
def get_pets(request):
    """Obtiene todas las mascotas disponibles en formato JSON"""
    if request.method == 'GET':
        pets = Pets.objects.filter(is_available=True)
        data = []
        for pet in pets:
            data.append({
                "id": pet.id,
                "name": pet.name,
                "breed": pet.breed.name if pet.breed else "Desconocido",
                "age": f"{pet.age} años" if pet.age else "Desconocida",
                "image": pet.image.url if pet.image else "https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&w=200&q=80",
                "distance": "A 5 km de ti" # Mock para mantener el diseño UI actual
            })
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        # Crear mascota desde Flutter
        try:
            body = json.loads(request.body)
            pet = Pets.objects.create(
                name=body.get('name'),
                description=body.get('breed', ''),
                # Asignamos valores predeterminados para que pase el modelo
                owner_id=1, 
                breed_id=1,
                is_available=True
            )
            return JsonResponse({"id": pet.id, "name": pet.name, "breed": body.get('breed'), "image": body.get('image')}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def get_my_pets(request):
    """Obtiene mascotas (mock para el usuario 1 en este ejemplo)"""
    if request.method == 'GET':
        pets = Pets.objects.filter(owner_id=1) 
        data = []
        for pet in pets:
            data.append({
                "id": pet.id,
                "name": pet.name,
                "breed": pet.breed.name if pet.breed else "Desconocido",
                "age": f"{pet.age} años" if pet.age else "Desconocida",
                "image": pet.image.url if pet.image else "https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&w=200&q=80",
            })
        return JsonResponse(data, safe=False)

@csrf_exempt
def delete_pet(request, pk):
    """Elimina una mascota dada su PK"""
    if request.method == 'DELETE':
        try:
            pet = Pets.objects.get(pk=pk)
            pet.delete()
            return JsonResponse({"message": "Eliminado exitosamente"})
        except Pets.DoesNotExist:
            return JsonResponse({"error": "No encontrado"}, status=404)

@csrf_exempt
def login_api(request):
    """Mock de login para Flutter"""
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            # Devuelve un token falso para engañar al frontend e ingresar
            return JsonResponse({"token": "fake-jwt-token-12345"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)