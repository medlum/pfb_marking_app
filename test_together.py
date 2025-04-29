import streamlit as st
import os
from together import Together

client = Together(api_key="a6eefc607a95354bef80535b2f3fb64f1d4ff0aa538a5f3fd3d83c34f1aa053e")

placeholder = st.empty()

stream = client.chat.completions.create(
model="meta-llama/Llama-3-8b-chat-hf",
messages=[{"role": "user", "content": "What are some fun things to do in New York?"}],
stream=True,
)

collected_response = ""
for chunk in stream:
    collected_response += chunk.choices[0].delta.content
    placeholder.text(collected_response)

