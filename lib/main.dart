import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(const PetMatchApp());
}

const String baseUrl = 'http://127.0.0.1:8000/api';

class PetMatchApp extends StatelessWidget {
  const PetMatchApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Pet Match',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.pink,
          primary: Colors.pinkAccent,
          secondary: Colors.purpleAccent,
        ),
        scaffoldBackgroundColor: Colors.grey[100],
        useMaterial3: true,
      ),
      home: const LoginScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}

// --- PANTALLA DE LOGIN ---
class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _isLoading = false;

  void _login() async {
    final email = _emailController.text;
    final password = _passwordController.text;

    if (!email.contains('@')) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('El correo debe contener un "@"')),
      );
      return;
    }

    if (password.length <= 5) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('La contraseña debe tener más de 5 caracteres'),
        ),
      );
      return;
    }

    setState(() => _isLoading = true);

    // Intenta hacer login con la API de Django (si está encendida)
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/login/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({"username": email, "password": password}),
      );
      // Ignoramos el resultado estricto para que puedas entrar aunque el server esté caído
    } catch (e) {
      // Ignorar error de red para continuar con la app
    }

    await Future.delayed(const Duration(milliseconds: 500));
    setState(() => _isLoading = false);

    if (mounted) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => const MainNavigator()),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(Icons.pets, size: 80, color: Colors.pinkAccent),
                const SizedBox(height: 16),
                const Text(
                  'Pet Match',
                  style: TextStyle(
                    fontSize: 32,
                    fontWeight: FontWeight.bold,
                    color: Colors.pinkAccent,
                  ),
                ),
                const SizedBox(height: 8),
                const Text('Encuentra la pareja ideal para tu mascota'),
                const SizedBox(height: 48),
                TextField(
                  controller: _emailController,
                  decoration: InputDecoration(
                    labelText: 'Correo Electrónico',
                    prefixIcon: const Icon(Icons.email),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  keyboardType: TextInputType.emailAddress,
                ),
                const SizedBox(height: 16),
                TextField(
                  controller: _passwordController,
                  decoration: InputDecoration(
                    labelText: 'Contraseña',
                    prefixIcon: const Icon(Icons.lock),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  obscureText: true,
                ),
                const SizedBox(height: 24),
                SizedBox(
                  width: double.infinity,
                  height: 50,
                  child: ElevatedButton(
                    onPressed: _isLoading ? null : _login,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.pinkAccent,
                      foregroundColor: Colors.white,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                    child: _isLoading
                        ? const CircularProgressIndicator(color: Colors.white)
                        : const Text(
                            'Iniciar Sesión',
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                  ),
                ),
                TextButton(
                  onPressed: () {},
                  child: const Text('¿No tienes cuenta? Regístrate'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

// --- NAVEGADOR PRINCIPAL (Bottom Nav) ---
class MainNavigator extends StatefulWidget {
  const MainNavigator({super.key});

  @override
  State<MainNavigator> createState() => _MainNavigatorState();
}

class _MainNavigatorState extends State<MainNavigator> {
  int _currentIndex = 0;

  final List<Widget> _screens = [
    const PetFeedScreen(),
    const MatchesScreen(),
    const ProfileScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _screens[_currentIndex],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _currentIndex,
        onDestinationSelected: (index) {
          setState(() {
            _currentIndex = index;
          });
        },
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.explore_outlined),
            selectedIcon: Icon(Icons.explore),
            label: 'Descubrir',
          ),
          NavigationDestination(
            icon: Icon(Icons.favorite_border),
            selectedIcon: Icon(Icons.favorite, color: Colors.pinkAccent),
            label: 'Matches',
          ),
          NavigationDestination(
            icon: Icon(Icons.person_outline),
            selectedIcon: Icon(Icons.person),
            label: 'Mi Perfil',
          ),
        ],
      ),
    );
  }
}

// --- PANTALLA PRINCIPAL (FEED DE MASCOTAS) ---
class PetFeedScreen extends StatefulWidget {
  const PetFeedScreen({super.key});

  @override
  State<PetFeedScreen> createState() => _PetFeedScreenState();
}

class _PetFeedScreenState extends State<PetFeedScreen> {
  List<dynamic> pets = [];
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchPets();
  }

  Future<void> _fetchPets() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/mascotas/'));
      if (response.statusCode == 200) {
        setState(() {
          pets = jsonDecode(response.body);
          isLoading = false;
        });
      } else {
        throw Exception('Error al cargar mascotas');
      }
    } catch (e) {
      setState(() => isLoading = false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Usando modo local (Backend apagado o inaccesible)'),
          ),
        );
        // Fallback a datos locales
        setState(() {
          pets = [
            {
              "id": 1,
              "name": "Max",
              "breed": "Golden Retriever",
              "image":
                  "https://images.unsplash.com/photo-1552053831-71594a27632d?auto=format&fit=crop&w=800&q=80",
              "age": "2 años",
              "distance": "A 5 km de ti",
            },
            {
              "id": 2,
              "name": "Luna",
              "breed": "Gato Persa",
              "image":
                  "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?auto=format&fit=crop&w=800&q=80",
              "age": "1 año",
              "distance": "A 2 km de ti",
            },
            {
              "id": 3,
              "name": "Rocky",
              "breed": "Bulldog Francés",
              "image":
                  "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?auto=format&fit=crop&w=800&q=80",
              "age": "3 años",
              "distance": "A 8 km de ti",
            },
          ];
        });
      }
    }
  }

  void _removePet(int index, String action) {
    final petName = pets[index]['name'];
    setState(() {
      pets.removeAt(index);
    });

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(
          action == 'like'
              ? '¡Le diste Me Gusta a $petName! 💖'
              : 'Pasaste a $petName',
        ),
        duration: const Duration(seconds: 1),
        behavior: SnackBarBehavior.floating,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          '🐶 Pet Match 🐱',
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
        centerTitle: true,
        elevation: 0,
        backgroundColor: Colors.white,
      ),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : pets.isEmpty
          ? const Center(
              child: Text(
                'No hay más mascotas cerca de ti',
                style: TextStyle(fontSize: 18, color: Colors.grey),
              ),
            )
          : ListView.builder(
              padding: const EdgeInsets.all(16.0),
              itemCount: pets.length,
              itemBuilder: (context, index) {
                final pet = pets[index];
                return Card(
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(20),
                  ),
                  elevation: 4,
                  margin: const EdgeInsets.only(bottom: 24),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      ClipRRect(
                        borderRadius: const BorderRadius.vertical(
                          top: Radius.circular(20),
                        ),
                        child: Image.network(
                          pet["image"] ?? "https://via.placeholder.com/400",
                          height: 350,
                          width: double.infinity,
                          fit: BoxFit.cover,
                          errorBuilder: (context, error, stackTrace) =>
                              Container(
                                height: 350,
                                color: Colors.grey[300],
                                child: const Icon(Icons.pets, size: 50),
                              ),
                        ),
                      ),
                      Padding(
                        padding: const EdgeInsets.all(16.0),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  '${pet["name"]}, ${pet["age"] ?? ""}',
                                  style: const TextStyle(
                                    fontSize: 24,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                const SizedBox(height: 4),
                                Text(
                                  pet["breed"] ?? "Desconocido",
                                  style: TextStyle(
                                    fontSize: 16,
                                    color: Colors.grey[700],
                                  ),
                                ),
                              ],
                            ),
                            Row(
                              children: [
                                Container(
                                  decoration: BoxDecoration(
                                    shape: BoxShape.circle,
                                    color: Colors.red[50],
                                  ),
                                  child: IconButton(
                                    icon: const Icon(
                                      Icons.close,
                                      color: Colors.redAccent,
                                      size: 30,
                                    ),
                                    onPressed: () => _removePet(index, 'pass'),
                                  ),
                                ),
                                const SizedBox(width: 12),
                                Container(
                                  decoration: BoxDecoration(
                                    shape: BoxShape.circle,
                                    color: Colors.green[50],
                                  ),
                                  child: IconButton(
                                    icon: const Icon(
                                      Icons.favorite,
                                      color: Colors.green,
                                      size: 30,
                                    ),
                                    onPressed: () => _removePet(index, 'like'),
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                );
              },
            ),
    );
  }
}

// --- PANTALLA DE MATCHES ---
class MatchesScreen extends StatelessWidget {
  const MatchesScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final List<Map<String, String>> matches = [
      {
        "name": "Bela",
        "image":
            "https://images.unsplash.com/photo-1537151608828-ea2b11777ee8?auto=format&fit=crop&w=200&q=80",
        "message": "¿Cuándo los juntamos en el parque?",
      },
      {
        "name": "Simba",
        "image":
            "https://images.unsplash.com/photo-1573865526739-10659fec78a5?auto=format&fit=crop&w=200&q=80",
        "message": "¡Hola! Mi gato es muy dócil.",
      },
    ];

    return Scaffold(
      appBar: AppBar(title: const Text('Tus Matches 💖'), centerTitle: true),
      body: ListView.separated(
        itemCount: matches.length,
        separatorBuilder: (context, index) => const Divider(),
        itemBuilder: (context, index) {
          final match = matches[index];
          return ListTile(
            leading: CircleAvatar(
              radius: 30,
              backgroundImage: NetworkImage(match["image"]!),
            ),
            title: Text(
              match["name"]!,
              style: const TextStyle(fontWeight: FontWeight.bold),
            ),
            subtitle: Text(match["message"]!),
            trailing: const Icon(
              Icons.chat_bubble_outline,
              color: Colors.pinkAccent,
            ),
            onTap: () {
              ScaffoldMessenger.of(
                context,
              ).showSnackBar(const SnackBar(content: Text('Abriendo chat...')));
            },
          );
        },
      ),
    );
  }
}

// --- PANTALLA DE PERFIL / AGREGAR MASCOTA ---
class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  List<dynamic> myPets = [];
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchMyPets();
  }

  Future<void> _fetchMyPets() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/mis-mascotas/'));
      if (response.statusCode == 200) {
        setState(() {
          myPets = jsonDecode(response.body);
          isLoading = false;
        });
      } else {
        throw Exception('Error al cargar');
      }
    } catch (e) {
      setState(() {
        isLoading = false;
        // Fallback mockup
        myPets = [
          {
            "id": 99,
            "name": "Toby",
            "breed": "Beagle",
            "age": "4 años",
            "image":
                "https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&w=200&q=80",
          },
        ];
      });
    }
  }

  Future<void> _addPet(Map<String, String> pet) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/mascotas/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(pet),
      );
      if (response.statusCode == 201 || response.statusCode == 200) {
        final newPet = jsonDecode(response.body);
        setState(() {
          myPets.add(newPet);
        });
      } else {
        // Fallback local si falla la API
        setState(() {
          myPets.add({...pet, "id": DateTime.now().millisecondsSinceEpoch});
        });
      }
    } catch (e) {
      setState(() {
        myPets.add({...pet, "id": DateTime.now().millisecondsSinceEpoch});
      });
    }
  }

  Future<void> _removePet(int index, int petId) async {
    try {
      await http.delete(Uri.parse('$baseUrl/mascotas/$petId/'));
      setState(() {
        myPets.removeAt(index);
      });
    } catch (e) {
      setState(() {
        myPets.removeAt(index);
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Mi Perfil'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () {
              Navigator.pushReplacement(
                context,
                MaterialPageRoute(builder: (context) => const LoginScreen()),
              );
            },
          ),
        ],
      ),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                children: [
                  const CircleAvatar(
                    radius: 50,
                    backgroundColor: Colors.pinkAccent,
                    child: Icon(Icons.person, size: 50, color: Colors.white),
                  ),
                  const SizedBox(height: 16),
                  const Text(
                    'Usuario',
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                  ),
                  const Text(
                    'Dueño verificado',
                    style: TextStyle(color: Colors.green),
                  ),
                  const SizedBox(height: 32),

                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text(
                        'Mis Mascotas Registradas',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      TextButton.icon(
                        icon: const Icon(Icons.add),
                        label: const Text('Añadir'),
                        onPressed: () {
                          _showAddPetDialog(context);
                        },
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),

                  ...myPets.asMap().entries.map((entry) {
                    int idx = entry.key;
                    var pet = entry.value;
                    return Card(
                      child: ListTile(
                        leading: ClipRRect(
                          borderRadius: BorderRadius.circular(8),
                          child: Image.network(
                            pet["image"] ?? "https://via.placeholder.com/150",
                            width: 50,
                            height: 50,
                            fit: BoxFit.cover,
                            errorBuilder: (context, error, stackTrace) =>
                                const Icon(Icons.pets),
                          ),
                        ),
                        title: Text(pet["name"] ?? "Sin nombre"),
                        subtitle: Text(
                          '${pet["breed"] ?? "Desconocido"} • ${pet["age"] ?? "?"}\nVacunas al día ✅',
                        ),
                        isThreeLine: true,
                        trailing: IconButton(
                          icon: const Icon(
                            Icons.delete,
                            color: Colors.redAccent,
                          ),
                          onPressed: () => _removePet(idx, pet["id"] ?? 0),
                        ),
                      ),
                    );
                  }),
                ],
              ),
            ),
    );
  }

  void _showAddPetDialog(BuildContext context) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) {
        return AddPetForm(onAdd: _addPet);
      },
    );
  }
}

class AddPetForm extends StatefulWidget {
  final Function(Map<String, String>) onAdd;
  const AddPetForm({super.key, required this.onAdd});

  @override
  State<AddPetForm> createState() => _AddPetFormState();
}

class _AddPetFormState extends State<AddPetForm> {
  final _nameController = TextEditingController();
  final _breedController = TextEditingController();
  final _ageController = TextEditingController();
  final _imageController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(
        bottom: MediaQuery.of(context).viewInsets.bottom,
        left: 16,
        right: 16,
        top: 24,
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          const Text(
            'Registrar Nueva Mascota',
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 24),

          TextField(
            controller: _imageController,
            decoration: InputDecoration(
              labelText: 'URL de la foto (Opcional)',
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
              ),
            ),
          ),
          const SizedBox(height: 16),
          TextField(
            controller: _nameController,
            decoration: InputDecoration(
              labelText: 'Nombre de la mascota',
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
              ),
            ),
          ),
          const SizedBox(height: 16),
          TextField(
            controller: _breedController,
            decoration: InputDecoration(
              labelText: 'Raza / Especie',
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
              ),
            ),
          ),
          const SizedBox(height: 16),
          TextField(
            controller: _ageController,
            decoration: InputDecoration(
              labelText: 'Edad',
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
              ),
            ),
          ),
          const SizedBox(height: 24),
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.pinkAccent,
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(vertical: 16),
            ),
            onPressed: () {
              if (_nameController.text.isEmpty) {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('El nombre es obligatorio')),
                );
                return;
              }
              widget.onAdd({
                "name": _nameController.text,
                "breed": _breedController.text.isNotEmpty
                    ? _breedController.text
                    : "Desconocido",
                "age": _ageController.text.isNotEmpty
                    ? _ageController.text
                    : "Desconocida",
                "image": _imageController.text.isNotEmpty
                    ? _imageController.text
                    : "https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&w=200&q=80",
              });
              Navigator.pop(context);
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Guardando mascota...')),
              );
            },
            child: const Text('Guardar Perfil'),
          ),
          const SizedBox(height: 24),
        ],
      ),
    );
  }
}
