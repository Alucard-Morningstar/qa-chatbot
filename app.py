import streamlit as st
import os
import openai
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

### Langsmith tracking

os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "True"
os.environ["LANGCHAIN_PROJECT"] = "Q&A Chatbot"

### Prompt Template

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant, Respond to the user queries in brief"),
        ("user", "Question: {question}")
    ]
)

def generate_response(question, api_key, llm, temp, max_tokens):
    openai.api_key = api_key
    llm = ChatOpenAI(model=llm)
    output_parser = StrOutputParser
    chain = prompt | llm | output_parser

    answer = chain.invoke({'question': question})

    return answer

## Webapp

st.title("Q&A Chatbot")

st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Open AI API Key", type = "password")

llm = st.sidebar.selectbox("Select a model", ["4o", "4 turbo", '3.5-turbo'])

### parameter setup
temperature =   st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value = 0.5)
max_tokens =   st.sidebar.slider("MAX Tokens",   max_value=300, min_value=50, value= 150)

### User input

st.write("Ask Question")
user_input  = st.text_input("You: ")

if user_input:
    response = generate_response(user_input, api_key, llm, temperature, max_tokens)
    st.write(response)
else:
    st.write("Please input a query")