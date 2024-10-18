# from dataclasses import dataclass
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
import getpass
import os
from dotenv import load_dotenv

from langchain_community.agent_toolkits.sql.base import create_sql_agent #
from langchain.agents.agent_types import AgentType
from langchain_community.utilities import SQLDatabase #
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import tool
from langchain import hub



db_sqlite = SQLDatabase.from_uri("sqlite:///recetas.db")

llm = GoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)

# Crear el SQL Agent
sql_agent = create_sql_agent(
    llm=llm,
    db=db_sqlite,
    verbose=True
)

# Load the environment variables
load_dotenv()

# Set the Google API key
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")


CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
If you don't know the answer, you can say "I don't know."
"""

memory = []
def chat(question):
    global memory
    PROMPT_TEMPLATE1 = """
        Hi there! I'm your culinary assistant, always ready to help you in the kitchen. 
        Please use the following information to answer the question:

        {context}

        ---
        Here's some context from our previous interactions:
        {memory}
        ---
        Please respond to the question based on the information above: {question}

        ### Response Format:
        - Provide a clear and concise answer based on the context.
        - Offer any additional tips or related information if relevant.
        - Do not include any headings or labels in the response.

        Remember to answer in Spanish and be kind and friendly in your tone. 
        If you don't know the answer, you can say "I don't know", but always with a smile.
    """


    # Prepare the DB.
    embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = Chroma(collection_name="Recetas",persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search(question, k=3)
    
    memory_text = "\n\n---\n\n".join(memory)
    context_text = "\n\n---\n\n".join([doc.page_content for doc in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE1)
    prompt = prompt_template.format(context=context_text, question=question, memory=memory_text)
    print(prompt)

    model = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    response_text = model.invoke(prompt)
    memory.append(f"Pregunta: {question}\nRespuesta: {response_text.content}")

    """ sources = [doc.metadata.get("source", None) for doc in results]
    formatted_response = f"{response_text.content}\nSources: {sources}"
    print(formatted_response) """
    return response_text.content
    

def main():
    # Create CLI.
    
    query_text = "Dame los ingredientes para hacer unos Tacos de Carnitas y como se prepara?."

    # Prepare the DB.
    embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = Chroma(collection_name="Recetas",persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search(query_text, k=3)
    

    context_text = "\n\n---\n\n".join([doc.page_content for doc in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)

    model = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("source", None) for doc in results]
    formatted_response = f"Response: {response_text.content}\nSources: {sources}"
    print(formatted_response)




    # Definir la función que maneja las consultas a ChromaDB
    def query_chroma(question: str):
        docs = db.similarity_search(question)
        return docs[0].page_content if docs else "No se encontró información relevante."

    # Crear herramienta para ChromaDB
    @tool
    def query_chroma(question: str) -> str:
        """Realiza una búsqueda semántica en ChromaDB para encontrar información relevante sobre recetas."""
        docs = db.similarity_search(question)
        return docs[0].page_content if docs else "No se encontró información relevante."
    

    # Usar el agente SQL para consultas más estructuradas
    tools = [query_chroma, sql_agent]
    prompt = hub.pull("hwchase17/react")

    # Inicializar agente combinando el SQL Agent y las herramientas para ChromaDB
    # Inicializar agente combinando el SQL Agent y las herramientas para ChromaDB
    agent = create_react_agent(
        tools=tools,
        llm=llm,
        prompt=prompt,
    )
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    # Pregunta sobre el número de recetas en la base de datos (SQL)
    question = "¿Cuántas recetas hay en total?"
    agent_executor.invoke({"input": question})

