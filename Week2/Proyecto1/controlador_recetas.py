import sqlite3
from init_sqlite import obtener_conexion


def create_table():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recetas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            ingredientes TEXT NOT NULL,
            procedimiento TEXT NOT NULL
        )
    ''')
    conexion.commit()
    conexion.close()


# Insertar receta en SQLite
def save_recipe(nombre, ingredientes, procedimiento):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    # Verificar si la receta ya existe
    cursor.execute('''
        SELECT id FROM recetas WHERE nombre = ?
    ''', (nombre,))
    
    receta_existente = cursor.fetchone()
    
    if receta_existente is None:
        # Si no existe, insertamos la nueva receta
        cursor.execute('''
            INSERT INTO recetas (nombre, ingredientes, procedimiento)
            VALUES (?, ?, ?)
        ''', (nombre, ingredientes, procedimiento))
        conexion.commit()
        print(f"Receta '{nombre}' insertada en la base de datos.")
    else:
        print(f"Receta '{nombre}' ya existe en la base de datos. No se inserta de nuevo.")
    conexion.close()


# Consultar nombres de recetas desde la base de datos SQLite
def query_NAME_recipes():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM recetas')
    recetas = cursor.fetchall()  # Cambiado a fetchall() para obtener todas las recetas
    print(f"Número total de recetas en la base de datos: {len(recetas)}")
    print("Recetas:")
    for receta in recetas:
        print(receta[1])
    conexion.close()

def get_recipes():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM recetas')
    recetas = cursor.fetchall()
    conexion.close()
    return recetas
    
def get_recipes_by_Ingredients(ingredientes):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    ingredientes_str = '%' + '%'.join(ingredientes) + '%'
    
    cursor.execute('''
        SELECT * FROM recetas 
        WHERE ingredientes LIKE ?
    ''', (ingredientes_str,))
    
    recetas = cursor.fetchall()
    
    # Usar un conjunto para evitar duplicados
    receta_vistas = set()
    for receta in recetas:
        if receta not in receta_vistas:
            receta_vistas.add(receta)
    
    conexion.close()
    return list(receta_vistas)