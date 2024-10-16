from load_docs import documents
from langchain_google_genai import GoogleGenerativeAIEmbeddings,ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

#Cargando la API de Google
load_dotenv()
API = os.getenv("GOOGLE_API_KEY")

#Dividiendo los documentos
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=0,
    length_function=len
)
texts = text_splitter.split_documents(documents)

#creando el vectorstore
vectorstore = Chroma.from_documents(documents=texts, embedding=GoogleGenerativeAIEmbeddings(model="models/embedding-001"))
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})

#Configurando el asistente
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

system_promt= (
    "Eres un asistente experto en responder preguntas sobre recetas de comida o cocina. "
    "Usa la información de contexto que te proporciono para responder a la pregunta. "
    "Si no sabes la respuesta, di 'No lo sé'. "
    "Intenta ser conciso.\n\n"
    "{context}"
)

promt = ChatPromptTemplate.from_template(
    "Eres un asistente experto en la area de cocina. Usa el contexto proporcionado para responder la pregunta.\n"
    "{context}\nPregunta: {input}\n"
)

while True:
    query = input("Soy tu asistente de cocina en que puedo ayudarte: ")
    if query.lower() == "salir":
        break
    else:
        question_answer_chain = create_stuff_documents_chain(llm, promt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        response = rag_chain.invoke({"input": query})
        print(response["answer"])