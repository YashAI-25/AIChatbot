# import os

# from groq import Groq
# from dotenv import load_dotenv

# load_dotenv()
# query = input("Enter your query: ")
# text=f"You are a chatbot designed to answer questions specifically related to [News]. Please make sure that your responses are always relevant to [News]. If a user asks a question that is not related to [Finance Expert], kindly respond with: 'I don't know.' "
# client = Groq(
#     api_key=os.environ.get("GROQ_API_KEY"),
# )

# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": text,
#         }
#     ],
#     model="llama-3.3-70b-versatile",
# )

# print(chat_completion.choices[0].message.content)

# frontend part

import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# Set page config
st.set_page_config(
    page_title="News Chatbot",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #f0f2f5;
    }
    .main .block-container {
        padding-top: 2rem;
    }
    .stChat {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .stChatMessage {
        background-color: #f8f9fa;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .stTextInput {
        background-color: white;
        border-radius: 10px;
        padding: 10px;
    }
    .stButton>button {
        background-color: #1a73e8;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1557b0;
    }
    .sidebar .sidebar-content {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .css-1d391kg {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Load environment variables
load_dotenv()

# Initialize Groq client
try:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
except Exception as e:
    st.error(f"Error initializing Groq client: {str(e)}")
    st.stop()

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    st.markdown("---")
    
    # Model selection
    model = st.selectbox(
        "Select Model",
        ["llama-3.3-70b-versatile"],
        index=0
    )
    
    # Temperature slider
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Higher values make the output more random, lower values make it more deterministic"
    )
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", type="primary"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("""
    ### About
    This News Chatbot is powered by Groq's LLM and can answer questions about current events and news.
    
    ### Features
    - Real-time news updates
    - Current events analysis
    - News-related queries
    - Historical news context
    
    ### Tips
    - Ask specific questions about news topics
    - Include dates for historical context
    - Request summaries of current events
    """)

# Main content
col1, col2 = st.columns([1, 2])

with col1:
    st.image("https://img.icons8.com/color/96/000000/news.png", width=100)
    st.title("📰 News Chatbot")
    st.markdown("Ask me anything about news and current events!")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Add welcome message if chat is empty
if not st.session_state.messages:
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I'm your News Chatbot. I can help you with questions about current events and news. How can I assist you today?"
    })

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about news..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Prepare the context for the chatbot
                text = f"You are a chatbot designed to answer questions specifically related to [News]. Please make sure that your responses are always relevant to [News]. If a user asks a question that is not related to [Finance Expert], kindly respond with: 'I don't know.' "
                
                # Get response from Groq
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": text},
                        {"role": "user", "content": prompt}
                    ],
                    model=model,
                    temperature=temperature
                )
                
                response = chat_completion.choices[0].message.content
                st.markdown(response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "I apologize, but I encountered an error. Please try again."
                })

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Built with ❤️ using Streamlit and Groq</p>
    <p>© 2024 News Chatbot</p>
</div>
""", unsafe_allow_html=True)