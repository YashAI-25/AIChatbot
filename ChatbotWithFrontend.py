import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(page_title="AI Chat Assistant", layout="wide")

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Main title
st.title("🤖 AI Chat Assistant")

# Create a text input for user query
user_query = st.text_input("Enter your question:", placeholder="What would you like to know?")

# Create a button to submit
if st.button("Ask AI"):
    if user_query:
        with st.spinner('Getting response...'):
            # Make API call to Groq
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": user_query,
                    }
                ],
                model="llama-3.3-70b-versatile",
            )
            
            # Display the response
            st.write("### Response:")
            st.write(chat_completion.choices[0].message.content)
    else:
        st.warning("Please enter a question!")

# Add a sidebar with information
with st.sidebar:
    st.header("About")
    st.write("This is an AI chat assistant powered by Groq API.")
    st.markdown("---")
    st.markdown("Built with Streamlit and Groq")

# Add expander for usage instructions
with st.expander("How to use"):
    st.write("""
    1. Type your question in the text box
    2. Click 'Ask AI' button
    3. Wait for the response
    """)