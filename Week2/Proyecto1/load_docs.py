from langchain.schema import Document
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
import getpass
import os
import shutil
from dotenv import load_dotenv
import sqlite3
import re

# Load the environment variables
load_dotenv()

# Set the Google API key
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

CHROMA_PATH = "chroma"
DATA_PATH = "static/data"

# Configurar base de datos SQLite
def create_db():
    conn = sqlite3.connect('recetas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recetas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            ingredientes TEXT,
            procedimiento TEXT
        )
    ''')
    conn.commit()
    return conn, cursor

# Insertar receta en SQLite
def save_recipe_to_db(cursor, nombre, ingredientes, procedimiento):
    cursor.execute('''
        INSERT INTO recetas (nombre, ingredientes, procedimiento)
        VALUES (?, ?, ?)
    ''', (nombre, ingredientes, procedimiento))

# Extraer recetas del texto completo utilizando expresiones regulares
def extract_recipes(full_text):
    pattern = r'(\d+\.\s+[^\n]+)\nIngredientes:\s*([\s\S]+?)Procedimiento:\s*([\s\S]+?)(?=\d+\.\s|\Z)'
    matches = re.findall(pattern, full_text)

    recipes = []
    for match in matches:
        name = match[0].strip()
        ingredients = match[1].strip().split('\n•')
        ingredients = [ingredient.strip() for ingredient in ingredients if ingredient.strip()]
        procedure = match[2].strip().split('\n')
        procedure = [step.strip() for step in procedure if step.strip()]
        
        if ingredients and procedure:
            recipes.append({
                'name': name,
                'ingredients': ingredients,
                'procedure': procedure
            })

    return recipes

# Generar la base de datos de documentos y almacenarlos
def generate_data_store():
    try:
        conn, cursor = create_db()
        documents = load_documents()
        if not documents:
            print("No documents loaded.")
            return
        chunks = split_text(documents, cursor)
        save_to_chroma(chunks)
        conn.commit()  # Guardar cambios en la base de datos
        conn.close()   # Cerrar conexión
    except Exception as e:
        print(f"Error during data store generation: {e}")

# Cargar documentos PDF de la carpeta
def load_documents():
    try:
        loader = PyPDFDirectoryLoader(DATA_PATH)
        documents = loader.load()
        print(f"Loaded {len(documents)} documents from {DATA_PATH}.")

        return documents
    except Exception as e:
        print(f"Error loading documents: {e}")
        return []

# Dividir el texto en chunks para su almacenamiento
def split_text(documents: list[Document], cursor):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=200,
        length_function=len,
        add_start_index=True,
        is_separator_regex=False
    )
    chunks = text_splitter.split_documents(documents)

    full_text = ""
    for doc in documents:
        full_text += doc.page_content + "\n\n"

    recipes = extract_recipes(full_text)

    for recipe in recipes:
        ingredients = "\n".join(recipe['ingredients']).strip()
        procedimiento = "\n".join(recipe['procedure']).strip()
        save_recipe_to_db(cursor, recipe['name'], ingredients, procedimiento)

    return chunks

# Guardar los chunks en la base de datos de Chroma
def save_to_chroma(chunks: list[Document]):
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    db = Chroma(
        collection_name="Recetas",
        embedding_function=GoogleGenerativeAIEmbeddings(model="models/embedding-001"),
        persist_directory=CHROMA_PATH
    )
    db.add_documents(chunks)
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

# Consultar las recetas en la base de datos según los ingredientes
def query_recipes_from_db(ingredientes):
    conn, cursor = create_db()
    ingredientes_str = '%' + '%'.join(ingredientes) + '%'
    
    cursor.execute('''
        SELECT nombre, ingredientes, procedimiento FROM recetas 
        WHERE ingredientes LIKE ?
    ''', (ingredientes_str,))
    
    recetas = cursor.fetchall()
    recetas_formateadas = []
    
    # Usar un conjunto para evitar duplicados
    receta_vistas = set()

    for receta in recetas:
        nombre, ingredientes, procedimiento = receta
        if nombre not in receta_vistas:
            receta_formateada = f"{nombre}\n\nIngredientes:\n{ingredientes}\n\nProcedimiento:\n{procedimiento}"
            recetas_formateadas.append(receta_formateada)
            receta_vistas.add(nombre)  # Marcar la receta como vista para evitar repetición
    
    conn.close()
    
    return recetas_formateadas

generate_data_store()
