import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

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
    full_response = ""
    for chunk in response:
        full_response += chunk.text  # Accumulate response chunks
    return full_response

# Initialize memory using LangChain
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Page configuration
st.set_page_config(
    page_title="Gemini LLM Q&A",
    page_icon="🤖",
    layout="wide"
)

# Header
st.title("🤖 ChatGPT Clone")

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

    # Add user's message to memory
    memory.save_context({"input": prompt}, {"output": ""})  # Empty output for now

    # Get response from the Gemini model
    with st.spinner("Generating response..."):
        ai_response = get_gemini_response(prompt)  # Get full response from the model

    # Display AI's response
    with st.chat_message("assistant"):
        st.markdown(f"**Bot:** {ai_response}")

    # Add the assistant's response to memory with explicit output_key
    memory.save_context({"input": prompt}, {"output": ai_response})  # Now we specify the output key

    # Update chat history
    st.session_state.chat_history.append(("user", prompt))
    st.session_state.chat_history.append(("assistant", ai_response))

    # Update memory with the new conversation
    memory.save_context({"input": prompt}, {"output": ai_response})  # Explicit output key