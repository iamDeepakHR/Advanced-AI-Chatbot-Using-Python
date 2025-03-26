from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = "YOUR_API_KEY"
if not api_key:
    st.error("API key not found. Please set the GENAI_API_KEY environment variable.")
    st.stop()

genai.configure(api_key=api_key)

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to get response from Gemini
def get_gemini_response(question):
    try:
        # Generate text using the correct model name
        response = model.generate_content(question)
        if response:
            parts = response.candidates[0].content.parts
            text = ' '.join(part.text for part in parts)
            if not text:
                return "No response available. Try Again."
            else:
                return text
    except Exception as e:
        return f"Error: {e}"

# Streamlit page configuration
st.set_page_config(
    page_title="Advanced Chatbot",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Main Title
st.markdown(
    """
    <div style='text-align: center;'>
        <h1>🤖 Advanced Chatbot</h1>
        <p>Ask me anything!</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Display chat history
for message in st.session_state["chat_history"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
user_question = st.chat_input("Type your question here...")

if user_question:
    # Add user message to chat history
    st.session_state["chat_history"].append({"role": "user", "content": user_question})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_question)

    # Get response from Gemini
    with st.spinner("Thinking..."):
        response = get_gemini_response(user_question)

    # Add assistant message to chat history
    st.session_state["chat_history"].append({"role": "assistant", "content": response})

    # Display assistant message
    with st.chat_message("assistant"):
        st.markdown(response)
