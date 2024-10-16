import os
import re
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFDirectoryLoader
import inflect  # Para manejar singularización de ingredientes

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración del LLM con la API de Google Gemini
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Crear un objeto de memoria para el contexto conversacional
memory = ConversationBufferMemory()

# Crear el modelo de lenguaje (LLM)
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.7,  # Se aumentó para respuestas más creativas
    max_tokens=256,
    timeout=None,
    max_retries=2,
)

# Integración con inflect para manejar pluralización/singularización
p = inflect.engine()

# Función para cargar documentos PDF de recetas
def load_documents(directory):
    loader = PyPDFDirectoryLoader(directory)
    documents = loader.load()
    return documents

# Función para limpiar cualquier numeración previa en los pasos
def limpiar_numeracion(texto):
    # Quitar números seguidos de punto o espacio al principio de cada línea
    return re.sub(r'^\d+\.\s*', '', texto, flags=re.MULTILINE)

# Función para buscar recetas según los ingredientes proporcionados
def buscar_recetas(ingredientes, documentos):
    recetas_encontradas = []
    
    for doc in documentos:
        contenido = doc.page_content.lower()

        # Verificar si todos los ingredientes proporcionados están en el contenido
        if all(ingrediente.lower() in contenido for ingrediente in ingredientes):
            # Buscar el nombre de la receta
            nombre_receta = re.search(r'(?:título|nombre|receta)[:\-]? (.+)', contenido)
            nombre_receta = nombre_receta.group(1).capitalize() if nombre_receta else "Receta sin nombre"

            # Extraer el procedimiento después de 'procedimiento:'
            if 'procedimiento:' in contenido:
                procedimiento = contenido.split('procedimiento:')[1].strip()
            else:
                procedimiento = "Procedimiento no disponible."

            # Limpiar cualquier numeración existente en los pasos
            procedimiento = limpiar_numeracion(procedimiento)

            # Separar los pasos correctamente
            pasos = procedimiento.split('. ')
            pasos_formateados = "\n".join([f"{i+1}. {paso.strip().capitalize()}." for i, paso in enumerate(pasos) if paso])

            # Formatear la receta con nombre y pasos
            receta_formateada = f"**{nombre_receta}**\n\n{pasos_formateados}\n"
            recetas_encontradas.append(receta_formateada)
    
    return recetas_encontradas if recetas_encontradas else ["No se encontraron recetas con esos ingredientes."]

# Ruta de los documentos de recetas
base_path = os.path.dirname(__file__)
data_path = os.path.join(base_path, "data")
documentos_recetas = load_documents(data_path)
