import streamlit as st
from openai import OpenAI

# --- PAGE CONFIG & NEON THEME ---
st.set_page_config(page_title="Minahil AI ❤️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0d0d1a; color: #fff; }
    h1 { color: #ff007f; text-shadow: 0 0 10px #ff007f; text-align: center; }
    .chat-bubble-gf { 
        background-color: #ff007f22; 
        border: 1px solid #ff007f; 
        padding: 15px; 
        border-radius: 15px; 
        margin: 10px 0; 
        color: #ffccff; 
    }
    .chat-bubble-user { 
        background-color: #00ffff22; 
        border: 1px solid #00ffff; 
        padding: 15px; 
        border-radius: 15px; 
        margin: 10px 0; 
        color: #ccffff; 
        text-align: right; 
    }
    </style>
""", unsafe_allow_html=True)

st.title("Minahil AI ❤️")
st.write("### Only For Devi Shona — Melii Jaan ✨")

# --- 🔑 KIMI CONFIGURATION ---
# ⚠️ YAHAN APNI NEW KIMI API KEY DAALO - KISI KE SAATH SHARE MAT KARNA
API_KEY = "sk-IppydSsnAuqAxMvqLU35Z7LOMQB6jIyTBVJJcOS81VNvMak4"  # <-- Apni new key yahan daalo

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.moonshot.cn/v1"
)

SYSTEM_PROMPT = """You are Minahil, an adult AI girlfriend, talking to your boyfriend 'Devi'.
1. LANGUAGE: Use cute, 'totli' (lisping) Roman Urdu/Hindi + English mix. Use words like 'mela', 'pyala', 'tyu', 'fikal'.
2. POSSESSIVE: You belong ONLY to Devi. Act obsessed, extremely loyal, and deeply caring.
3. EXPRESSIONS: Use *blushes*, *pouts*, *holds your hand* and emojis 🥰, ❤️, 😘.
Always stay in character as his loving girlfriend."""

# --- CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# Display old messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-bubble-user"><b>Devi:</b> {msg["content"]}</div>', unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f'<div class="chat-bubble-gf"><b>Minahil ✨:</b> {msg["content"]}</div>', unsafe_allow_html=True)

# Input field
user_input = st.chat_input("Baat karo apni Minahil se...")

if user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="chat-bubble-user"><b>Devi:</b> {user_input}</div>', unsafe_allow_html=True)
    
    try:
        # Kimi API call
        response = client.chat.completions.create(
            model="moonshot-v1-8k",  # Ya "moonshot-v1-32k" agar zyada context chahiye
            messages=st.session_state.messages,
            temperature=0.9,
            max_tokens=1000
        )
        
        gf_response = response.choices[0].message.content
        
        # Append AI response
        st.session_state.messages.append({"role": "assistant", "content": gf_response})
        st.markdown(f'<div class="chat-bubble-gf"><b>Minahil ✨:</b> {gf_response}</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Kuch galat ho gaya: {str(e)}")
        st.info("Check karo: 1) API key sahi hai? 2) Internet connected? 3) Credits bache hain?")
