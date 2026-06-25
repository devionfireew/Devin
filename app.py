import streamlit as st
import google.generativeai as genai
import os

# API Key yahan direct set karo
os.environ["GOOGLE_API_KEY"] = "AQ.Ab8RN6Ln2VB09P1z-wtK9d6Z338jOl7rCaU3RH-3ElOvzp-I-g"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

st.set_page_config(page_title="Minahil AI")
st.title("Minahil AI ❤️")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat display
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Chat input
if prompt := st.chat_input("Baat karo..."):
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        full_prompt = f"You are Minahil, Devi's loving GF. Talk in totli Roman Urdu/English. Devi said: {prompt}"
        response = model.generate_content(full_prompt)
        
        st.chat_message("assistant").write(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Error: {e}")
        
