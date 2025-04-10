import os
import streamlit as st
import pandas as pd
import speech_recognition as sr
import pyttsx3
import queue
import threading
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.schema import Document
from PIL import Image
import threading
# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not GROQ_API_KEY or not HUGGINGFACE_API_KEY:
    st.error("API keys not found. Please check your .env file.")
    st.stop()

# Set environment variables
os.environ["GROQ_API_KEY"] = GROQ_API_KEY
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

# Streamlit Page Config
st.set_page_config(page_title="AI-Powered Cancer Support", layout="wide")
st.title("")

# File Path for Disease Data
disease_file_path = r'C:\Users\LETS\PycharmProjects\pythonProject\Medical_Chatbot\pdf\data.csv'
persist_directory = "doc1_db"

# Function to Load CSV File as Documents
def load_csv_as_documents(file_path):
    try:
        df = pd.read_csv(file_path, encoding="utf-8")
        return [Document(page_content=str(row.to_dict()), metadata={"index": idx}) for idx, row in df.iterrows()]
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return []

# Load & Process Documents
documents = load_csv_as_documents(disease_file_path)
if not documents:
    st.stop()

# Split text into chunks
text_splitter = CharacterTextSplitter(chunk_size=2500, chunk_overlap=500)
text_chunks = text_splitter.split_documents(documents)

# Initialize Embeddings & Vector Store
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

if os.path.exists(persist_directory) and os.listdir(persist_directory):
    vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embedding)
else:
    vectorstore = Chroma.from_documents(
        documents=text_chunks,
        embedding=embedding,
        persist_directory=persist_directory
    )
    vectorstore.persist()

# Set up Retriever & Chat Model
retriever = vectorstore.as_retriever()
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

# Initialize QA Chain
try:
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
except Exception as e:
    st.error(f"Failed to initialize qa_chain: {e}")
    st.stop()

# Initialize Chat History
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


def speak_text(text):
    """Create a new engine instance to avoid threading issues."""
    def run_speech():
        engine = pyttsx3.init(driverName='sapi5')  # New instance every time
        engine.say(text)
        engine.runAndWait()
        engine.stop()  # Ensure cleanup

    speech_thread = threading.Thread(target=run_speech, daemon=True)
    speech_thread.start()




def recognize_speech():
    """Capture voice input and convert to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            st.success(f"🎤 You said: {text}")
            return text
        except sr.UnknownValueError:
            st.error("😕 Sorry, I couldn't understand. Please try again.")
        except sr.RequestError:
            st.error("🚨 Speech recognition service error.")
        return None

# Voice Response Toggle
voice_response = st.toggle("🔊 Enable Voice Response")

# UI Layout for Chat Input & Voice Button in the Same Line
col1, col2 = st.columns([0.8, 0.2])

with col1:
    query = st.chat_input("🔎 Enter your question:")

with col2:
    if st.button("🎙️"):
        voice_query = recognize_speech()
        if voice_query:
            query = voice_query  # Assigning voice query to text query

# Process User Query
if query:
    with st.spinner("🤖 Processing..."):
        try:
            response = qa_chain.invoke({"query": query})
            answer = response["result"]

            # Store in chat history
            st.session_state["chat_history"].append({"query": query, "response": answer})

            # Display User Query
            st.write("#### User:")
            st.markdown(f'<div style="background-color: white; color: black; padding: 10px; border-radius: 5px;">{query}</div>', unsafe_allow_html=True)

            # Display AI Response
            st.write("#### Response:")
            st.markdown(f'<div style="background-color: white; color: black; padding: 10px; border-radius: 5px;">{answer}</div>', unsafe_allow_html=True)

            # Speak the response if enabled
            if voice_response:
                speak_text(answer)
        except Exception as e:
            st.error(f"Error processing query: {e}")

# Display Chat History in Sidebar
st.sidebar.write("🗂️ **Chat History**")
for chat in st.session_state["chat_history"]:
    with st.sidebar.expander(f"🗨️ {chat['query']}"):
        st.write(f"**Response:** {chat['response']}")

print("success")
