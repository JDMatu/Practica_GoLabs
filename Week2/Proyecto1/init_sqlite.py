import sqlite3


# Configurar base de datos SQLite
def obtener_conexion():
    return sqlite3.connect('recetas.db')

