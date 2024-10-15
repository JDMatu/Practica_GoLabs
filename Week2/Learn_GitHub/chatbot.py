import os
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
import inflect  # Para manejar singularización de ingredientes

# Configuración del LLM con la API de Google Gemini
os.environ["GOOGLE_API_KEY"] = "AIzaSyBj-k3Lw5M3I6P7oS7mapqTPTyg6s-YlyM"

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