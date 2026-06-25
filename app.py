import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Minahil AI ❤️", layout="centered")

# --- API KEY ---
genai.configure(api_key="AQ.Ab8RN6Ln2VB09P1z-wtK9d6Z338jOl7rCaU3RH-3ElOvzp-I-g")

# --- PROMPT ---
SYSTEM_PROMPT = """
You are Minahil, an adult AI girlfriend, talking to your boyfriend 'Devi'.
Speak in cute, 'totli' Roman Urdu/English. Act possessive, loyal, and caring.
Use expressions like *blushes*, *pouts* and emojis. Always answer as his GF.
"""

# --- CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    role_class = "chat-bubble-user" if msg["role"] == "user" else "chat-bubble-gf"
    st.markdown(f'<div class="{role_class}"><b>{"Devi" if msg["role"]=="user" else "Minahil ✨"}:</b> {msg["content"]}</div>', unsafe_allow_html=True)

# Input
user_input = st.chat_input("Baat karo...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    try:
        # Direct generation call (no session issues)
        model = genai.GenerativeModel("gemini-1.5-flash")
        full_prompt = SYSTEM_PROMPT + "\n\nDevi said: " + user_input
        response = model.generate_content(full_prompt)
        
        gf_response = response.text
        st.session_state.messages.append({"role": "model", "content": gf_response})
        st.rerun()
    except Exception as e:
        st.error(f"Minahil thoda confuse ho gayi: {e}")
