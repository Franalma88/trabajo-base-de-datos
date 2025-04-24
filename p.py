import sqlite3
import requests
import time
import timeit

# Conectar a la base de datos
conexion = sqlite3.connect("pokemon.db")
cursor = conexion.cursor()

# Crear la tabla si no existe
cursor.execute("""
    CREATE TABLE IF NOT EXISTS pokemons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        altura INTEGER,
        peso INTEGER,
        tipos TEXT
    )
""")
conexion.commit()

# Función para obtener y guardar 20 Pokémon
def guardar_pokemones(limit=20):
    url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        for pokemon in data['results']:
            detalle = requests.get(pokemon['url']).json()
            nombre = detalle['name'].capitalize()
            altura = detalle['height']
            peso = detalle['weight']
            tipos = ', '.join([t['type']['name'] for t in detalle['types']])

            cursor.execute("SELECT * FROM pokemons WHERE nombre = ?", (nombre,))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO pokemons (nombre, altura, peso, tipos)
                    VALUES (?, ?, ?, ?)
                """, (nombre, altura, peso, tipos))
                conexion.commit()
        print(" Pokémon guardados en la base de datos.")
    else:
        print(" Error al conectarse a la PokeAPI.")

# Mostrar Pokémon guardados
def mostrar_pokemones():
    cursor.execute("SELECT * FROM pokemons")
    for fila in cursor.fetchall():
        print(fila)

# Modificar un Pokémon
def modificar_pokemon():
    mostrar_pokemones()
    id_pokemon = input("🔧 Introduce el ID del Pokémon que deseas modificar: ")

    cursor.execute("SELECT * FROM pokemons WHERE id = ?", (id_pokemon,))
    pokemon = cursor.fetchone()

    if pokemon:
        nuevo_nombre = input(f"Nuevo nombre (actual: {pokemon[1]}): ") or pokemon[1]
        nueva_altura = input(f"Nueva altura (actual: {pokemon[2]}): ") or pokemon[2]
        nuevo_peso = input(f"Nuevo peso (actual: {pokemon[3]}): ") or pokemon[3]

        try:
            nueva_altura = int(nueva_altura)
            nuevo_peso = int(nuevo_peso)

            cursor.execute("""
                UPDATE pokemons
                SET nombre = ?, altura = ?, peso = ?
                WHERE id = ?
            """, (nuevo_nombre, nueva_altura, nuevo_peso, id_pokemon))
            conexion.commit()
            print(" Datos actualizados correctamente.")
        except ValueError:
            print(" Altura y peso deben ser números.")
    else:
        print(" No se encontró ningún Pokémon con ese ID.")

# -------------------------------------
# Bloque principal con medición de tiempo
# -------------------------------------
if __name__ == "__main__":
    # Medir tiempo real con time
    inicio = time.time()
    guardar_pokemones()
    fin = time.time()
    print(f"\n Tiempo real (time): {fin - inicio:.2f} segundos")

    # Medir tiempo promedio con timeit (una sola ejecución)
    duracion = timeit.timeit("guardar_pokemones()", globals=globals(), number=1)
    print(f"Tiempo con timeit: {duracion:.2f} segundos")

    pepe = input("\n¿Quieres que muestre los Pokémon guardados? (si/no): ").strip().lower()
    if pepe == "si":
        mostrar_pokemones()

    maripuri = input("¿Quieres modificar algún Pokémon? (si/no): ").strip().lower()
    if maripuri == "si":
        print("\n Lista antes de modificar:")
        mostrar_pokemones()

        modificar_pokemon()

        print("\n Lista después de modificar:")
        mostrar_pokemones()

    conexion.close()
