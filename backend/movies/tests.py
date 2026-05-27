from django.test import TestCase
from django.contrib.auth.models import User
from .models import Breeds, Pets
from datetime import date


class BreedsTestCase(TestCase):
    """Tests para el modelo Breeds"""
    
    def setUp(self):
        Breeds.objects.create(
            name='Labrador',
            description='Perro amigable y leal',
            characteristics='Grande, energético, excelente nadador'
        )

    def test_breed_creation(self):
        breed = Breeds.objects.get(name='Labrador')
        self.assertEqual(breed.description, 'Perro amigable y leal')


class PetsTestCase(TestCase):
    """Tests para el modelo Pets"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.breed = Breeds.objects.create(
            name='Labrador',
            description='Raza de perro'
        )
        self.pet = Pets.objects.create(
            owner=self.user,
            breed=self.breed,
            name='Max',
            gender='M',
            birth_date=date(2020, 1, 1),
            description='Perro saludable',
            image='pets/test.jpg'
        )

    def test_pet_creation(self):
        pet = Pets.objects.get(name='Max')
        self.assertEqual(pet.owner, self.user)
        self.assertEqual(pet.breed, self.breed)

    def test_pet_age_calculation(self):
        age = self.pet.age()
        self.assertGreaterEqual(age, 4)
