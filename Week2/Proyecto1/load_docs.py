from langchain_community.document_loaders import PyPDFDirectoryLoader
import os

def load_documents (directory):
    loader = PyPDFDirectoryLoader(directory)
    document = loader.load()
    return document

#Crea la ruta absoluta del directorio o carpeta donde se encuentran los documentos
base_path = os.path.dirname(__file__) 
dir_path = os.path.join(base_path, "data")
#Carga los documentos
documents = load_documents(dir_path)
