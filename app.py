import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini Pro model and chat object
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Function to get responses from the Gemini model
def get_gemini_response(question):
    """
    Fetches the response from the Gemini model for a given question.
    The response is streamed in chunks for real-time updates.
    """
    response = chat.send_message(question, stream=True)
    return response

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Page configuration
st.set_page_config(
    page_title="Gemini LLM Q&A",
    page_icon="🤖",
    layout="wide"
)

# Header
st.title("🤖 Gemini LLM Chat Application")

# Display chat history
st.subheader("Chat History")
for message in st.session_state.chat_history:
    role, text = message
    with st.chat_message(role):
        st.markdown(f"**{role}:** {text}")

# User input area
if prompt := st.chat_input("Enter your question here..."):
    # Display user's message
    with st.chat_message("user"):
        st.markdown(f"**You:** {prompt}")

    # Get response from the Gemini model
    with st.spinner("Generating response..."):
        response_chunks = get_gemini_response(prompt)
        ai_response = ""
        for chunk in response_chunks:
            ai_response += chunk.text  # Combine all response chunks

    # Display AI's response
    with st.chat_message("assistant"):
        st.markdown(f"**Bot:** {ai_response}")

    # Update chat history
    st.session_state.chat_history.append(("user", prompt))
    st.session_state.chat_history.append(("assistant", ai_response))