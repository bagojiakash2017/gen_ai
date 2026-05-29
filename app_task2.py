import streamlit as st
import os
from google import genai
from dotenv import load_dotenv, find_dotenv

# Load your .env file
load_dotenv(find_dotenv())

# App Title
st.title("🎨 Task 2: Creative Visionary Engine")
st.write("Verifying API connection using Gemini 2.0 Flash.")

# Initialize the client
api_key = os.getenv("GEMINI_API_KEY")

if st.button("Check API and Generate Concept"):
    if not api_key:
        st.error("API Key not found in .env file!")
    else:
        try:
            client = genai.Client(api_key=api_key)
            
            # Using the robust gemini-2.0-flash model
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents="Describe a detailed, high-quality, cyberpunk-style corporate logo concept."
            )
            
            st.success("Connection Successful! Here is your generated concept:")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"Error: {e}")