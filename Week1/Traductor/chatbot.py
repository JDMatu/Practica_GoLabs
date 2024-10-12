import getpass
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate



# Set the Google API key
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")


# Create a language model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)


# Create a prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant that translates {input_language} to {output_language}.",
        ),
        ("human", "{input}"),
    ]
) 

# Create a chain
chain = prompt | llm

def chatbot(input_language, output_language, input_text):
    # Run the chain
    return chain.invoke(
        {
            "input_language": input_language,
            "output_language": output_language,
            "input": input_text,
        }
    )


