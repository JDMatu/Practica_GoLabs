from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.prompts import ChatPromptTemplate
import getpass
import os
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# Establecer la clave API de Google
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Introduce tu clave API de Google AI: ")

CHROMA_PATH = "chroma"

# Plantilla de prompts en español
PROMPT_TEMPLATE = """
Eres un asistente de cocina. Basándote en el siguiente contexto, responde a la pregunta del usuario de manera inteligente:

{context}

---

Aquí está la pregunta del usuario: {question}
Si no conoces la respuesta, puedes decir "No lo sé."
"""

# Función para manejar la consulta avanzada con LLM
def query_llm(pregunta: str):
    # Crear función de embeddings
    embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    # Conectar a la base de datos Chroma
    db = Chroma(collection_name="Recetas", persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    
    # Caso especial: si el usuario pregunta por el número de recetas
    if "cuántas recetas" in pregunta.lower():
        return contar_total_recetas()

    # Realizar búsqueda en la base de datos usando la pregunta del usuario
    resultados = db.similarity_search(pregunta, k=3)
    
    # Generar contexto a partir de los resultados
    contexto = "\n\n---\n\n".join([doc.page_content for doc in resultados])
    
    # Crear el prompt basado en el contexto y la pregunta
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=contexto, question=pregunta)
    
    # Invocar el modelo LLM para generar una respuesta
    modelo = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    respuesta = modelo.invoke(prompt)
    
    # Obtener las fuentes usadas para la respuesta
    fuentes = [doc.metadata.get("source", None) for doc in resultados]
    respuesta_formateada = f"Respuesta: {respuesta.content}\nFuentes: {fuentes}"
    
    return respuesta_formateada

# Nueva función para contar el total de recetas
def contar_total_recetas():
    try:
        # Crear función de embeddings
        embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        
        # Conectar a la base de datos Chroma
        db = Chroma(collection_name="Recetas", persist_directory=CHROMA_PATH, embedding_function=embedding_function)
        
        # Obtener todos los documentos (recetas) de la base de datos
        todas_recetas = db.get()
        total_recetas = len(todas_recetas['documents'])
        
        # Devolver el resultado en español
        respuesta = f"Conozco un total de {total_recetas} recetas."
        return respuesta
    
    except Exception as e:
        return "Hubo un problema al contar las recetas."
