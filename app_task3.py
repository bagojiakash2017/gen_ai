import streamlit as st
import os
from dotenv import load_dotenv

# Use direct imports to avoid sub-module path issues
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

st.title("Knowledge Analyst: Simple Mode")

uploaded_file = st.file_uploader("Upload your PDF document", type="pdf")

if uploaded_file and api_key:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Process PDF
    loader = PyPDFLoader("temp.pdf")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)
    
    # Embedding and Vector Database
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
    db = Chroma.from_documents(texts, embeddings)
    
    # Directly query the database
    query = st.text_input("Ask a question about the PDF:")
    if query:
        with st.spinner("Searching and generating..."):
            # Simplify the interaction to avoid complex chain imports
            llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)
            docs = db.similarity_search(query)
            context = "\n".join([d.page_content for d in docs])
            
            response = llm.invoke(f"Based on this context: {context}\n\nAnswer: {query}")
            st.write("**Answer:**", response.content)
else:
    st.info("Please upload a PDF to start.")