# from dataclasses import dataclass
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.prompts import ChatPromptTemplate

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def main():
    # Create CLI.
    
    query_text = "What are the pricing for SmartCoop?"

    # Prepare the DB.
    embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = Chroma(collection_name="SmartCoop",persist_directory=CHROMA_PATH, embedding_function=embedding_function)

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
    response_text = model.predict(prompt)

    sources = [doc.metadata.get("source", None) for doc in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)


if __name__ == "__main__":
    main()