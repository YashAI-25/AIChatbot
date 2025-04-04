import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
import time
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Groq client
try:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
except Exception as e:
    st.error(f"Error initializing Groq client: {str(e)}")
    st.stop()

# Set page config with custom theme
st.set_page_config(
    page_title="Finance Expert Chatbot",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
    }
    .stTextInput>div>div>input {
        background-color: white;
        border-radius: 10px;
        padding: 10px;
    }
    .stMarkdown {
        font-family: 'Helvetica Neue', sans-serif;
    }
    .chat-message {
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f5f5f5;
        border-left: 4px solid #4caf50;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        padding: 10px;
        background-color: #2196f3;
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1976d2;
        transform: translateY(-2px);
    }
    .topic-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 5px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    .topic-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Header section with enhanced styling
st.title("💰 Finance Expert Chatbot")
st.markdown("""
    <div style='background-color: #e3f2fd; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
        <h3 style='color: #1976d2;'>Welcome to your Personal Finance Assistant!</h3>
        <p>Ask me anything about finance, and I'll provide expert insights and guidance.</p>
        <p style='font-size: 0.9em; color: #666;'>Current time: {}</p>
    </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history with improved styling
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(f"""
            <div class='chat-message {message["role"]}-message'>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)

# Chat input with improved styling
if prompt := st.chat_input("Ask me anything about finance..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(f"""
            <div class='chat-message user-message'>
                {prompt}
            </div>
            """, unsafe_allow_html=True)

    # Get chatbot response with typing effect
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a chatbot designed to answer questions specifically related to Finance Expert. Please make sure that your responses are always relevant to Finance. If a user asks a question that is not related to Finance, kindly respond with: 'I can only answer questions related to finance. Please ask a finance-related question.'"
                        },
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model="llama-3.3-70b-versatile",
                )
                response = chat_completion.choices[0].message.content
                st.markdown(f"""
                    <div class='chat-message assistant-message'>
                        {response}
                    </div>
                    """, unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "I apologize, but I encountered an error. Please try again."
                })

# Sidebar with additional features
with st.sidebar:
    st.title("About")
    st.markdown("""
        <div style='background-color: #e3f2fd; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <h3 style='color: #1976d2;'>Finance Expert Chatbot</h3>
            <p>Powered by Groq's LLM technology</p>
            <p style='font-size: 0.9em; color: #666;'>Your trusted financial advisor</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Topics I can help with:")
    topics = [
        "📈 Investment Strategies",
        "💼 Market Analysis",
        "💰 Personal Finance",
        "🏦 Banking",
        "📊 Financial Planning",
        "💳 Credit Management",
        "🏠 Real Estate Investment",
        "📱 Digital Banking"
    ]
    
    for topic in topics:
        st.markdown(f"""
            <div class='topic-card'>
                {topic}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", type="primary"):
            st.session_state.messages = []
            st.rerun()
    
    with col2:
        if st.button("📥 Export Chat", type="secondary"):
            chat_text = "\n\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
            st.download_button(
                label="Download Chat",
                data=chat_text,
                file_name=f"finance_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
    
    st.markdown("---")
    st.markdown("""
        <div style='font-size: 0.8em; color: #666;'>
            <p>Need help? Contact support</p>
            <p>Version 1.0.0</p>
            <p>Last updated: {}</p>
        </div>
    """.format(datetime.now().strftime("%Y-%m-%d")), unsafe_allow_html=True)