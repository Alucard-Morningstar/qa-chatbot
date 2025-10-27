from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

### Langsmith tracking

os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Q&A Chatbot - Ollama(gemma 3)"

## prompt template

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant, Respond to the user queries in brief"),
        ("user", "Question: {question}")
    ]
)


def generate_response(question, engine, temp, max_tok):

    llm = Ollama(model = engine)
    output_parser = StrOutputParser()

    chain =  prompt|llm|output_parser

    answer = chain.invoke({'question': question})

    return answer

## Webapp

st.title("Q&A Chatbot with Gemma 3")

st.sidebar.title("Settings")

### parameter setup
temperature =   st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value = 0.5)
max_tokens =   st.sidebar.slider("MAX Tokens",   max_value=300, min_value=50, value= 150)

### User input

st.write("Ask Question")
user_input  = st.text_input("You: ")

if user_input:
    response = generate_response(user_input, "gemma3:1b", temperature, max_tokens)
    st.write(response)
else:
    st.write("Please input a query")
