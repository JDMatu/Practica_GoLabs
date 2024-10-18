from langchain.schema import Document
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
import getpass
import os
import shutil
from dotenv import load_dotenv
import re
import controlador_recetas

# Load the environment variables
load_dotenv()


# Set the Google API key
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

CHROMA_PATH = "chroma"
DATA_PATH = "static/data"




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


def generate_data_store():
    try:
        documents = load_documents()
        if not documents:
            print("No documents loaded.")
            return
        chunks = split_text(documents)
        save_to_chroma(chunks)
    except Exception as e:
        print(f"Error during data store generation: {e}")

def load_documents():
    try:
        loader = PyPDFDirectoryLoader(DATA_PATH)
        documents = loader.load()
        print(f"Loaded {len(documents)} documents from {DATA_PATH}.")
        return documents
    except Exception as e:
        print(f"Error loading documents: {e}")
        return []

def split_text(documents: list[Document]):
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


    # Extraer y guardar información de múltiples recetas
    recipes = extract_recipes(full_text)

    for recipe in recipes:
        name = recipe['name'].split('.')[1].strip()
        ingredients = ""
        for ingredient in recipe['ingredients']:
            ingredients += f"{ingredient}\n"
        ingredients = ingredients.strip()
        procedimiento = ""
        for step in recipe['procedure']:
            procedimiento += f"{step}\n"
        procedimiento = procedimiento.strip()

        controlador_recetas.save_recipe(name, ingredients, procedimiento)


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


controlador_recetas.query_NAME_recipes()