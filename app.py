import streamlit as st
import google.generativeai as genai

# API Key
API_KEY = "AQ.Ab8RN6LO1cYSWm_WD47cJ8zD-kzwm1beSRcNP0XjG2M0NNhvaw"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="Minahil AI ❤️", layout="centered")

st.title("Minahil AI ❤️")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
if prompt := st.chat_input("Baat karo..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        # Model naam change kiya hai
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content(f"You are Minahil, Devi's GF. Be cute, possessive and talk in totli Urdu/English. Devi said: {prompt}")
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Error: {e}")
