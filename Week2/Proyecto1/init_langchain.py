from load_docs import documents
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
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
resultados = vectorstore.similarity_search("jugo de limon", k=5)
for resultado in resultados:
    print(resultado)