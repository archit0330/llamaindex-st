import streamlit as st
import openai
from llama_index.llms.openai import OpenAI
try:
  from llama_index import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader
except ImportError:
  from llama_index.core import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader

st.set_page_config(page_title="Hi! welcome to onlinePadhayi.com", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)
openai.api_key = st.secrets.openai_key
st.title("Hi! welcome to onlinePadhayi.com")
# st.info("Check out the full tutorial to build this app in our [blog post](https://blog.streamlit.io/build-a-chatbot-with-custom-data-sources-powered-by-llamaindex/)", icon="📃")
         
if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        # {"role": "assistant", "content": "Ask me a question about Streamlit's open-source Python library!"}
        {"role": "assistant", "content": "Ask me a question about Online MBA"}
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing the Streamlit docs – hang tight! This should take 1-2 minutes."):

        # CHANGE DATA ROUTE
        reader = SimpleDirectoryReader(input_dir="./mba_data", recursive=True)
        docs = reader.load_data()
        # llm = OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are an expert o$
        # index = VectorStoreIndex.from_documents(docs)

        # CHANGE SYSTEM PROMPT
        service_context = ServiceContext.from_defaults(llm=OpenAI(
            model="gpt-3.5-turbo", 
            temperature=0.5, 
            system_prompt=
            """You are a education counsellor with knowledge about online degree programs offered by universities mentioned in the document provided. 
            Rules:
            1. Only give answers based on the uploaded document
            2. Always address the user with "Learner"
            3. At the end mention the website link for the university who's question is about.
            4. Don't say "based on the document" or "from the document". 
            Keep your answers technical and based on facts – do not hallucinate features.
                """))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index

index = load_data()

if "chat_engine" not in st.session_state.keys(): # Initialize the chat engine
        st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history
