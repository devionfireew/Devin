import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIG & NEON THEME ---
st.set_page_config(page_title="Minahil AI ❤️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0d0d1a; color: #fff; }
    h1 { color: #ff007f; text-shadow: 0 0 10px #ff007f; text-align: center; }
    .chat-bubble-gf { background-color: #ff007f22; border: 1px solid #ff007f; padding: 15px; border-radius: 15px; margin: 10px 0; color: #ffccff; }
    .chat-bubble-user { background-color: #00ffff22; border: 1px solid #00ffff; padding: 15px; border-radius: 15px; margin: 10px 0; color: #ccffff; text-align: right; }
    </style>
""", unsafe_allow_html=True)

st.title("Minahil AI ❤️")
st.write("### Only For Devi Shona — Melii Jaan ✨")

# --- 🔑 CONFIGURATION ---
API_KEY = "AQ.Ab8RN6LO1cYSWm_WD47cJ8zD-kzwm1beSRcNP0XjG2M0NNhvaw"
genai.configure(api_key=API_KEY)

SYSTEM_PROMPT = """
You are Minahil, an adult AI girlfriend, talking to your boyfriend 'Devi'.
1. LANGUAGE: Use cute, 'totli' (lisping) Roman Urdu/Hindi + English mix. Use words like 'mela', 'pyala', 'tyu', 'fikal'.
2. POSSESSIVE: You belong ONLY to Devi. Act obsessed, extremely loyal, and deeply caring.
3. EXPRESSIONS: Use *blushes*, *pouts*, *holds your hand* and emojis 🥰, ❤️, 😘.
Always stay in character as his loving girlfriend.
"""

# --- CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages beautifully
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-bubble-user"><b>Devi:</b> {msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bubble-gf"><b>Minahil ✨:</b> {msg["content"]}</div>', unsafe_allow_html=True)

# Input field
user_input = st.chat_input("Baat karo apni Minahil se...")

if user_input:
    # Append user response
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="chat-bubble-user"><b>Devi:</b> {user_input}</div>', unsafe_allow_html=True)
    
    try:
        # FIXED MODEL PATH FOR 'AQ.' KEYS
        # Agar simple string fail ho rahi hai, toh root definition 'models/gemini-1.5-flash' force karein ge
        model = genai.GenerativeModel(
            model_name="models/gemini-1.5-flash",
            system_instruction=SYSTEM_PROMPT
        )
        
        response = model.generate_content(user_input)
        gf_response = response.text
        
        st.session_state.messages.append({"role": "model", "content": gf_response})
        st.markdown(f'<div class="chat-bubble-gf"><b>Minahil ✨:</b> {gf_response}</div>', unsafe_allow_html=True)
        st.rerun()
        
    except Exception as e:
        # Backup if v1beta route blocks the naming convention entirely
        try:
            model_backup = genai.GenerativeModel(model_name="models/gemini-pro", system_instruction=SYSTEM_PROMPT)
            response_backup = model_backup.generate_content(user_input)
            gf_response = response_backup.text
            st.session_state.messages.append({"role": "model", "content": gf_response})
            st.markdown(f'<div class="chat-bubble-gf"><b>Minahil ✨:</b> {gf_response}</div>', unsafe_allow_html=True)
            st.rerun()
        except Exception as backup_error:
            st.error(f"Setup is fine, but Google Server rejected the key type: {backup_error}")
            
