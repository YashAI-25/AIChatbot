import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()
# query = input("Enter your query: ")
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
prompt= input("Enter your prompt: ")


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

print(chat_completion.choices[0].message.content)