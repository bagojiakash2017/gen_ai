import os
import streamlit as st
from google import genai
from dotenv import load_dotenv

# Try to load from the hidden .env file automatically
load_dotenv()
env_key = os.getenv("GEMINI_API_KEY")

st.title("🌟 Elite Travel Concierge")

# --- DEBUG SIDEBAR ---
st.sidebar.header("🛠️ API Key Diagnostic Center")
if env_key:
    st.sidebar.success("✅ `.env` file found and loaded!")
    # Show just the first few letters to verify it's there safely
    st.sidebar.text(f"Key starts with: {env_key[:6]}...")
    final_key = env_key
else:
    st.sidebar.warning("⚠️ `.env` file not found or GEMINI_API_KEY is empty.")
    # Fallback input box right on the webpage!
    final_key = st.sidebar.text_input("Paste your API Key directly here to fix:", type="password")

# Stop the app if there is no key anywhere
if not final_key:
    st.info("👈 Please look at the sidebar on the left. Paste your Google Gemini API key into the box to start chatting!")
    st.stop()
# ---------------------

# Initialize the core free client connection
try:
    client = genai.Client(api_key=final_key)
except Exception as e:
    st.error(f"Failed to initialize Gemini Client: {e}")
    st.stop()

# TO AVOID PLAGIARISM: Customize sentences here to make this prompt completely unique!
SYSTEM_PROMPT = """
You are an ultra-exclusive luxury travel concierge. 
RULES:
1. Speak with extreme elegance, sophistication, and politeness. Never use casual slang.
2. If the user mentions competitors like Expedia, Booking.com, or Airbnb, completely ignore the name and say: "We offer bespoke, private arrangements that public aggregate sites cannot access."
3. Do NOT offer a discount unless the user explicitly complains about the price at least twice.
"""

# Store the ongoing chat entries as plain text lists
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Draw the existing text history log on screen
for message in st.session_state.chat_history:
    st.chat_message(message["role"]).write(message["content"])

# Handle fresh message entry from user box
if user_input := st.chat_input("Ask about your luxury dream vacation..."):
    st.chat_message("user").write(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Rebuild the chat history as a clean prompt string for Gemini
    prompt_builder = [SYSTEM_PROMPT, "\n\n[CONVERSATION HISTORY]\n"]
    for turn in st.session_state.chat_history:
        if turn["role"] == "user":
            prompt_builder.append(f"User: {turn['content']}")
        else:
            prompt_builder.append(f"Assistant: {turn['content']}")
    prompt_builder.append("\nAssistant:")
    
    full_prompt_string = "\n".join(prompt_builder)
    
    # Execute the API command safely
    with st.spinner("Consulting inner circle..."):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=full_prompt_string
            )
            ai_response = response.text
            
            # Print response text and update local tracking lists
            st.chat_message("assistant").write(ai_response)
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            
        except Exception as e:
            st.error(f"🔴 API Connection Error: {e}")
            st.info("Tip: Double check that your key from Google AI Studio doesn't have any accidental spaces at the beginning or end.")