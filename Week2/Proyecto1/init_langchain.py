# from dataclasses import dataclass
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.prompts import ChatPromptTemplate
import getpass
import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Set the Google API key
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")


CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
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

memory = []
def main(query:str):
    # Create CLI.
    global memory
    query_text = query

    # Prepare the DB.
    embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = Chroma(collection_name="Recetas",persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    
    # Search the DB.
    
    results = db.similarity_search(query_text, k=29)
    
    
    memory_text = "\n\n---\n\n".join(memory)
    context_text = "\n\n---\n\n".join([doc.page_content for doc in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text, memory=memory_text)

    model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)
    response_text = model.invoke(prompt)
    memory.append(f"Pregunta: {query_text}\nRespuesta: {response_text.content}")

    
    formatted_response = f"{response_text.content}"
    return formatted_response


if __name__ == "__main__":
    main()