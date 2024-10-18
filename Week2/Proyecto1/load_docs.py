from langchain.schema import Document
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
import getpass
import os
import shutil
from dotenv import load_dotenv
<<<<<<< HEAD
import sqlite3
import re
=======
import re
import controlador_recetas
>>>>>>> fcd2359c054239ce14c8c099ae669ec14007c636

# Load the environment variables
load_dotenv()

<<<<<<< HEAD
# Variable para almacenar nombres de recetas
recipe_names = []
=======
>>>>>>> fcd2359c054239ce14c8c099ae669ec14007c636

# Set the Google API key
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

CHROMA_PATH = "chroma"
DATA_PATH = "static/data"


<<<<<<< HEAD
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
=======
>>>>>>> fcd2359c054239ce14c8c099ae669ec14007c636


def extract_recipes(full_text):
    # Definir un patrón para las recetas
    pattern = r'(\d+\.\s+[^\n]+)\nIngredientes:\s*([\s\S]+?)Procedimiento:\s*([\s\S]+?)(?=\d+\.\s|\Z)'
    
    matches = re.findall(pattern, full_text)

    recipes = []
    for match in matches:
        name = match[0].strip()
        ingredients = match[1].strip().split('\n•')
        ingredients = [ingredient.strip() for ingredient in ingredients if ingredient.strip()]  # Limpiar ingredientes
        procedure = match[2].strip().split('\n')
        procedure = [step.strip() for step in procedure if step.strip()]  # Limpiar pasos del procedimiento
        
        # Validar que hay ingredientes y procedimiento
        if ingredients and procedure:
            recipes.append({
                'name': name,
                'ingredients': ingredients,
                'procedure': procedure
            })

    return recipes


<<<<<<< HEAD


def generate_data_store():
    try:
        conn, cursor = create_db()
=======
def generate_data_store():
    try:
>>>>>>> fcd2359c054239ce14c8c099ae669ec14007c636
        documents = load_documents()
        if not documents:
            print("No documents loaded.")
            return
<<<<<<< HEAD
        chunks = split_text(documents,cursor)
        save_to_chroma(chunks)
        conn.commit()  # Guardar cambios en la base de datos
        conn.close()   # Cerrar conexión
=======
        chunks = split_text(documents)
        save_to_chroma(chunks)
>>>>>>> fcd2359c054239ce14c8c099ae669ec14007c636
    except Exception as e:
        print(f"Error during data store generation: {e}")

def load_documents():
    try:
        loader = PyPDFDirectoryLoader(DATA_PATH)
        documents = loader.load()
        print(f"Loaded {len(documents)} documents from {DATA_PATH}.")
<<<<<<< HEAD

=======
>>>>>>> fcd2359c054239ce14c8c099ae669ec14007c636
        return documents
    except Exception as e:
        print(f"Error loading documents: {e}")
        return []

<<<<<<< HEAD
def split_text(documents: list[Document], cursor):
=======
def split_text(documents: list[Document]):
>>>>>>> fcd2359c054239ce14c8c099ae669ec14007c636
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=200,
        length_function=len,
        add_start_index=True,
        is_separator_regex=False
    )
    chunks = text_splitter.split_documents(documents)

<<<<<<< HEAD
    # Imprimir detalles del primer chunk
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
    """ for i, chunk in enumerate(chunks):
        print(f"Chunk {i}: {chunk.page_content}")
        print("----------------------------------------------------------------------------------------") """
    
    # Concatenar el contenido de todos los documentos en una sola variable
    full_text = ""
    for doc in documents:
        full_text += doc.page_content + "\n\n"  # Añadir separador entre documentos

    print(f"Full text length: {len(full_text)}")
    print("----------------------------------------------------------------------------------------")
=======
    full_text = ""
    for doc in documents:
        full_text += doc.page_content + "\n\n"

>>>>>>> fcd2359c054239ce14c8c099ae669ec14007c636

    # Extraer y guardar información de múltiples recetas
    recipes = extract_recipes(full_text)

    for recipe in recipes:
<<<<<<< HEAD
=======
        name = recipe['name'].split('.')[1].strip()
>>>>>>> fcd2359c054239ce14c8c099ae669ec14007c636
        ingredients = ""
        for ingredient in recipe['ingredients']:
            ingredients += f"{ingredient}\n"
        ingredients = ingredients.strip()
        procedimiento = ""
        for step in recipe['procedure']:
            procedimiento += f"{step}\n"
        procedimiento = procedimiento.strip()
<<<<<<< HEAD
        
        
       #save_recipe_to_db(cursor, recipe['name'], ingredients, procedimiento)
        #recipe_names.append(recipe['name'])  # Guardar nombre en la lista
=======

        controlador_recetas.save_recipe(name, ingredients, procedimiento)
>>>>>>> fcd2359c054239ce14c8c099ae669ec14007c636


    return chunks



def save_to_chroma(chunks: list[Document]):
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create a new DB from the documents.
    db = Chroma(
        collection_name="Recetas",embedding_function=GoogleGenerativeAIEmbeddings(model="models/embedding-001"), persist_directory=CHROMA_PATH
    )
    db.add_documents(chunks)
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


<<<<<<< HEAD
generate_data_store()


# Consultar nombres de recetas desde la base de datos SQLite
def query_recipes_from_db():
    conn, cursor = create_db()
    cursor.execute('SELECT procedimiento FROM recetas where id = 1')
    recetas = cursor.fetchone()  # Cambiado a fetchall() para obtener todas las recetas
    print(f"Número total de recetas en la base de datos: {len(recetas)}")
    print(recetas)
    print("Nombres de las recetas en la base de datos:")
    """ for i, receta in enumerate(recetas, start=1):
        print(f"- {receta}")  # receta[1] contiene el nombre de la receta
        print("----------------------------------------------------------------------------------------") """
    conn.close()


query_recipes_from_db()
=======
controlador_recetas.query_NAME_recipes()
>>>>>>> fcd2359c054239ce14c8c099ae669ec14007c636
