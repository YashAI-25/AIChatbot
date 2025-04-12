import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stTextInput>div>div>input {
        background-color: white;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px;
        border-radius: 5px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .response-box {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
print("API KEY:", os.environ.get("GROQ_API_KEY"))
print(client)

# Main title with custom styling
st.markdown("<h1 style='text-align: center; color: #2c3e50;'>🤖 AI Chat Assistant</h1>", unsafe_allow_html=True)

# Create two columns for layout
col1, col2 = st.columns([2, 1])

with col1:
    # Chat interface
    st.markdown("### 💬 Chat with AI")
    
    # Initialize session state for chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get AI response
        with st.spinner('Thinking...'):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model="llama-3.3-70b-versatile",
                )
                
                response = chat_completion.choices[0].message.content
                
                # Add AI response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
                with st.chat_message("assistant"):
                    st.write(response)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

with col2:
    # Sidebar content
    st.markdown("### ℹ️ About")
    st.markdown("""
    This AI chat assistant is powered by:
    - Groq API
    - Streamlit
    - Llama 3.3 70B model
    """)
    
    st.markdown("### 📝 How to use")
    st.markdown("""
    1. Type your question in the chat box
    2. Press Enter or click Send
    3. Wait for the AI's response
    4. Continue the conversation
    """)
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
