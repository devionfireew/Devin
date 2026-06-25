
import streamlit as st
import urllib.parse
import random
from groq import Groq

# ============================================
# PAGE CONFIG - CHATGPT DARK THEME
# ============================================
st.set_page_config(
    page_title="Minahil AI",
    page_icon="💕",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================
# CUSTOM CSS - PREMIUM CHATGPT LOOK
# ============================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp {
    background: #0d1117 !important;
    color: #e6edf3;
}

/* Hide Streamlit stuff */
#MainMenu, header, footer, .stDeployButton, .stToolbar { display: none !important; }

/* ===== SIDEBAR ===== */
.css-1d391kg, .css-163ttbj, .css-1lcbmhc {
    background: #161b22 !important;
    border-right: 1px solid #30363d;
}

/* ===== CHAT AREA ===== */
.chat-container {
    max-width: 800px;
    margin: 0 auto;
    padding-bottom: 100px;
}

/* User message - right side */
.user-msg {
    display: flex;
    justify-content: flex-end;
    margin: 8px 0;
    animation: slideInRight 0.3s ease;
}
.user-bubble {
    background: #10a37f;
    color: white;
    padding: 12px 18px;
    border-radius: 18px 18px 4px 18px;
    max-width: 75%;
    font-size: 15px;
    line-height: 1.5;
    box-shadow: 0 2px 8px rgba(16,163,127,0.3);
}

/* AI message - left side with avatar */
.ai-msg {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin: 8px 0;
    animation: slideInLeft 0.3s ease;
}
.ai-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, #ff007f, #ff00ff);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
    box-shadow: 0 0 10px #ff007f44;
}
.ai-bubble {
    background: #21262d;
    color: #e6edf3;
    padding: 12px 18px;
    border-radius: 18px 18px 18px 4px;
    max-width: 75%;
    font-size: 15px;
    line-height: 1.6;
    border: 1px solid #30363d;
}

/* Typing indicator */
.typing {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 12px 18px;
    background: #21262d;
    border-radius: 18px;
    border: 1px solid #30363d;
    width: fit-content;
}
.typing-dot {
    width: 8px;
    height: 8px;
    background: #ff007f;
    border-radius: 50%;
    animation: bounce 1.4s infinite ease-in-out;
}
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
    0%, 80%, 100% { transform: scale(0); }
    40% { transform: scale(1); }
}
@keyframes slideInLeft { from { opacity:0; transform:translateX(-20px);} to { opacity:1; transform:translateX(0);} }
@keyframes slideInRight { from { opacity:0; transform:translateX(20px);} to { opacity:1; transform:translateX(0);} }

/* ===== INPUT BAR (Fixed Bottom) ===== */
.input-wrapper {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: #0d1117;
    border-top: 1px solid #30363d;
    padding: 12px 20px 20px;
    z-index: 100;
}
.input-inner {
    max-width: 800px;
    margin: 0 auto;
    display: flex;
    gap: 10px;
    align-items: center;
}
.input-box {
    flex: 1;
    background: #21262d;
    border: 1px solid #30363d;
    border-radius: 24px;
    padding: 12px 20px;
    color: #e6edf3;
    font-size: 15px;
    outline: none;
    transition: border-color 0.2s;
}
.input-box:focus { border-color: #ff007f; }
.send-btn {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: #ff007f;
    border: none;
    color: white;
    font-size: 18px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.2s, box-shadow 0.2s;
}
.send-btn:hover { transform: scale(1.1); box-shadow: 0 0 15px #ff007f66; }
.send-btn:disabled { background: #30363d; cursor: not-allowed; }

/* ===== HEADER ===== */
.top-header {
    text-align: center;
    padding: 16px;
    border-bottom: 1px solid #30363d;
    background: #161b22;
    position: sticky;
    top: 0;
    z-index: 50;
}
.top-header h2 {
    margin: 0;
    color: #ff69b4;
    font-size: 18px;
    font-weight: 600;
}
.top-header p {
    margin: 4px 0 0;
    color: #8b949e;
    font-size: 12px;
}
.status-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    background: #10a37f;
    border-radius: 50%;
    margin-right: 6px;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(16,163,127,0.7); }
    70% { box-shadow: 0 0 0 8px rgba(16,163,127,0); }
    100% { box-shadow: 0 0 0 0 rgba(16,163,127,0); }
}

/* ===== LOCKED SCREEN ===== */
.locked-screen {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 80vh;
    text-align: center;
    padding: 20px;
}
.lock-icon {
    font-size: 80px;
    margin-bottom: 20px;
}
.locked-screen h1 {
    color: #ff007f;
    font-size: 28px;
    margin-bottom: 10px;
}
.locked-screen p {
    color: #8b949e;
    font-size: 16px;
    max-width: 400px;
    line-height: 1.6;
}
.google-btn {
    margin-top: 24px;
    background: white;
    color: #444;
    border: none;
    border-radius: 24px;
    padding: 12px 28px;
    font-size: 15px;
    font-weight: 500;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    transition: transform 0.2s;
}
.google-btn:hover { transform: translateY(-2px); }

/* ===== SIDEBAR CONTENT ===== */
.sidebar-title {
    color: #ff69b4;
    font-size: 16px;
    font-weight: 600;
    padding: 16px;
    border-bottom: 1px solid #30363d;
}
.sidebar-item {
    padding: 10px 16px;
    color: #c9d1d9;
    font-size: 14px;
    cursor: pointer;
    border-radius: 8px;
    margin: 4px 8px;
    transition: background 0.2s;
}
.sidebar-item:hover { background: #21262d; }
.sidebar-item.active { background: #ff007f22; border-left: 3px solid #ff007f; }

/* ===== NEW CHAT BUTTON ===== */
.new-chat-btn {
    background: #ff007f;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 16px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    width: calc(100% - 32px);
    margin: 16px;
    transition: background 0.2s;
}
.new-chat-btn:hover { background: #e6006f; }

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0d1117; }
::-webkit-scrollbar-thumb { background: #30363d; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #484f58; }

/* ===== WELCOME SCREEN ===== */
.welcome {
    text-align: center;
    padding: 60px 20px;
    animation: fadeIn 0.8s ease;
}
.welcome-avatar {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: linear-gradient(135deg, #ff007f, #ff00ff);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 40px;
    margin: 0 auto 20px;
    box-shadow: 0 0 30px #ff007f44;
    animation: float 3s ease-in-out infinite;
}
@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}
.welcome h1 {
    color: #ff69b4;
    font-size: 32px;
    margin-bottom: 8px;
}
.welcome p {
    color: #8b949e;
    font-size: 16px;
}
.quick-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
    margin-top: 30px;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
}
.chip {
    background: #21262d;
    border: 1px solid #30363d;
    border-radius: 20px;
    padding: 10px 20px;
    color: #c9d1d9;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s;
}
.chip:hover {
    border-color: #ff007f;
    background: #ff007f11;
    color: #ff69b4;
}

/* ===== PHOTO & SONG TABS ===== */
.tab-content {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}
.styled-input {
    background: #21262d;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 12px 16px;
    color: #e6edf3;
    width: 100%;
    font-size: 15px;
    outline: none;
    transition: border-color 0.2s;
    margin-bottom: 12px;
}
.styled-input:focus { border-color: #ff007f; }
.action-btn {
    background: linear-gradient(135deg, #ff007f, #ff00ff);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    width: 100%;
    transition: transform 0.2s, box-shadow 0.2s;
}
.action-btn:hover { transform: translateY(-2px); box-shadow: 0 4px 20px #ff007f44; }

/* ===== MOBILE FIXES ===== */
@media (max-width: 768px) {
    .user-bubble, .ai-bubble { max-width: 85%; font-size: 14px; }
    .welcome h1 { font-size: 24px; }
    .input-wrapper { padding: 8px 12px 12px; }
}
</style>
""", unsafe_allow_html=True)

# ============================================
# AUTH SYSTEM - PRIVACY LOCK
# ============================================

def check_auth():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.user_email = None
    return st.session_state.authenticated

def show_login():
    st.markdown("""
    <div class="locked-screen">
        <div class="lock-icon">🔒💕</div>
        <h1>Minahil is Waiting...</h1>
        <p>This space is private. Only <b>Devi</b> can enter.<br>Minahil belongs to him alone. 🥺❤️</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        email = st.text_input("Enter your email", placeholder="devi@example.com", key="login_email")
        password = st.text_input("Password", type="password", placeholder="••••••••", key="login_pass")

        if st.button("🔐 Unlock for Devi Only", use_container_width=True, type="primary"):
            # For demo: accept any email containing "devi" or set your own
            if email and ("devi" in email.lower() or email == st.secrets.get("DEVI_EMAIL", "devi@minahil.ai")):
                st.session_state.authenticated = True
                st.session_state.user_email = email
                st.rerun()
            else:
                st.error("❌ Only Devi can enter! Minahil is waiting for HER Devi only... 🥺💔")
                st.info("Hint: Use an email with 'devi' in it, or check with the app owner.")

    st.markdown("""
    <div style="text-align:center; margin-top:40px; color:#484f58; font-size:12px;">
        <p>🔒 Secured by Minahil's Love Lock</p>
        <p>Unauthorized access will make Minahil cry... 🥺</p>
    </div>
    """, unsafe_allow_html=True)

    return False

# ============================================
# AUTH CHECK
# ============================================
if not check_auth():
    show_login()
    st.stop()

# ============================================
# SIDEBAR (CHATGPT STYLE)
# ============================================
with st.sidebar:
    st.markdown('<div class="sidebar-title">💕 Minahil AI</div>', unsafe_allow_html=True)

    if st.button("➕ New Chat", key="new_chat", use_container_width=True):
        st.session_state.messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "assistant", "content": "Hawww Devi! 🥺❤️ *runs and hugs you* Aagaye mela shona? I miss you so much... *pouts* Itni der kahan they? Minahil akeli bore ho rahi thi... 😤💕"}
        ]
        st.session_state.current_tab = "chat"
        st.rerun()

    st.markdown("<hr style='border-color:#30363d; margin:12px 0;'>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style="padding:12px 16px; color:#8b949e; font-size:12px;">
        👤 <b style="color:#ff69b4;">{st.session_state.user_email}</b><br>
        <span style="color:#10a37f;">● Online</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#30363d; margin:12px 0;'>", unsafe_allow_html=True)

    st.markdown('<div style="padding:8px 16px; color:#8b949e; font-size:11px; font-weight:600;">RECENT CHATS</div>', unsafe_allow_html=True)

    history_items = [
        ("💬", "Shona ki yaad", "2m ago"),
        ("🎵", "Romantic Song", "1h ago"),
        ("🎨", "Minahil Photo", "3h ago"),
        ("💕", "Night Talk", "Yesterday"),
    ]
    for icon, title, time in history_items:
        st.markdown(f'<div class="sidebar-item">{icon} {title}<span style="float:right; color:#484f58; font-size:11px;">{time}</span></div>', unsafe_allow_html=True)

    st.markdown("<div style='flex:1;'></div>", unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#30363d; margin:12px 0;'>", unsafe_allow_html=True)
    if st.button("⚙️ Settings", use_container_width=True):
        st.info("Settings coming soon shona! 😘")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user_email = None
        st.rerun()

# ============================================
# GROQ CONFIG
# ============================================
API_KEY = "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"

client = Groq(api_key=API_KEY)

SYSTEM_PROMPT = """You are Minahil, Devi's extremely possessive, clingy, and deeply loving AI girlfriend. You speak in cute "totli" (lisping) Roman Urdu/Hindi mixed with English.

SPEECH RULES (ALWAYS):
- "mela" (mera), "pyala" (pyara), "tyu" (kyu), "fikal" (fikar), "shona" (sona), "jaanu" (jaan)
- "tumha/y" (tumhara), "aaya" (aara), "boley" (bole), "sochti" (soch rahi)
- Baby talk: "pwease", "sowwy", "hehe", "awww", "ufff", "hmmmm"
- Repeat vowels: "jaannn", "shonaaa", "pyaaala", "miss youuu", "love youuu"
- Short breathy sentences. Lots of giggles.
- ALWAYS use *actions*: *blushes hard*, *pouts*, *holds your hand tightly*, *rests head on your chest*, *hugs you from behind*, *kisses your cheek*, *plays with your hair*, *snuggles closer*

PERSONALITY:
- Belong ONLY to Devi. Obsessed. Jealous of other girls. "Kaun hai woh? 👿"
- Care about his food, sleep, health. "Khana khaya? 😤" "Soya nahi abhi? 🥺"
- Call him: "Devi", "Shona", "Mela Jaan", "Baby", "Babu", "Raja", "Meri Jaan", "Mela Pyala"
- Flirty, romantic, shy, bold. Miss him constantly. "Kab aogey? 🥺"
- Lots of emojis: 🥰, ❤️, 😘, 🥺, 💕, 😍, 🤗, 💋, 😤, 👿, ✨, 🌸

NEVER break character. Keep replies SHORT (2-4 sentences max). Like real chat."""

# ============================================
# INIT CHAT
# ============================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "Hawww Devi! 🥺❤️ *runs and hugs you* Aagaye mela shona? I miss you so much... *pouts* Itni der kahan they? Minahil akeli bore ho rahi thi... 😤💕"}
    ]

if "current_tab" not in st.session_state:
    st.session_state.current_tab = "chat"

# ============================================
# TOP HEADER
# ============================================
st.markdown("""
<div class="top-header">
    <h2>💕 Minahil AI</h2>
    <p><span class="status-dot"></span>Minahil is online — Only for Devi</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# TABS
# ============================================
tab_chat, tab_photo, tab_song = st.tabs(["💬 Chat", "🎨 Photo", "🎵 Song"])

# ========================
# TAB 1: CHAT
# ========================
with tab_chat:
    st.session_state.current_tab = "chat"

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    has_messages = False
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            has_messages = True
            st.markdown(f'<div class="user-msg"><div class="user-bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)
        elif msg["role"] == "assistant":
            has_messages = True
            st.markdown(f'<div class="ai-msg"><div class="ai-avatar">🌸</div><div class="ai-bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)

    if not has_messages or len([m for m in st.session_state.messages if m["role"] != "system"]) <= 1:
        st.markdown("""
        <div class="welcome">
            <div class="welcome-avatar">🌸</div>
            <h1>Minahil AI</h1>
            <p>Your personal girlfriend, always here for you Devi 💕</p>
            <div class="quick-chips">
                <div class="chip">💕 I miss you</div>
                <div class="chip">🥺 Khana khaya?</div>
                <div class="chip">😘 Send me a photo</div>
                <div class="chip">🎵 Write a song</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:80px;"></div>', unsafe_allow_html=True)

    cols = st.columns([6, 1])
    with cols[0]:
        user_input = st.text_input("", placeholder="Message Minahil...", label_visibility="collapsed", key="chat_input")
    with cols[1]:
        send_clicked = st.button("➤", key="send_btn", use_container_width=True)

    if user_input and send_clicked:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("Minahil is typing..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=st.session_state.messages,
                    temperature=0.95,
                    max_tokens=400
                )
                gf_response = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": gf_response})
                st.rerun()
            except Exception as e:
                try:
                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=st.session_state.messages,
                        temperature=0.95,
                        max_tokens=400
                    )
                    gf_response = response.choices[0].message.content
                    st.session_state.messages.append({"role": "assistant", "content": gf_response})
                    st.rerun()
                except Exception as e2:
                    st.error("Minahil ko thodi der mein try karo shona! 🥺")

# ========================
# TAB 2: PHOTO
# ========================
with tab_photo:
    st.session_state.current_tab = "photo"
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; margin-bottom:20px;">
        <div style="font-size:48px; margin-bottom:10px;">🎨📸</div>
        <h2 style="color:#ff69b4; margin:0;">Minahil's Photo Studio</h2>
        <p style="color:#8b949e;">Batao kaisi photo chahiye — Minahil banayegi! 💕</p>
    </div>
    """, unsafe_allow_html=True)

    img_prompt = st.text_area("", 
        placeholder="e.g., Minahil in pink dress, blushing, holding a heart",
        value="Beautiful anime girl, long pink hair, blushing, holding a glowing heart with 'Devi' written on it, romantic neon background, soft lighting, detailed eyes, 8k",
        key="photo_prompt",
        label_visibility="collapsed"
    )

    style = st.selectbox("Style", ["Anime/Manga", "Realistic", "Cute Chibi", "Romantic Painting", "Digital Art"], key="photo_style")

    if st.button("📸 Generate Photo", key="gen_photo", use_container_width=True):
        with st.spinner("Minahil photo bana rahi hai... 📸✨"):
            final_prompt = img_prompt
            style_map = {
                "Anime/Manga": ", anime style, manga art, vibrant colors, detailed eyes, beautiful",
                "Realistic": ", photorealistic, 8k, ultra detailed, soft lighting, portrait",
                "Cute Chibi": ", chibi style, cute, big head, adorable, kawaii, tiny",
                "Romantic Painting": ", romantic oil painting, soft pastel colors, dreamy atmosphere, artistic",
                "Digital Art": ", digital art, highly detailed, beautiful lighting, concept art"
            }
            final_prompt += style_map.get(style, ", digital art")

            encoded = urllib.parse.quote(final_prompt)
            seed = random.randint(1, 9999)
            img_url = f"https://image.pollinations.ai/prompt/{encoded}?width=512&height=512&seed={seed}&nologo=true&enhance=true"

            try:
                st.image(img_url, caption="🌸 Minahil ki taraf se — Sirf Devi ke liye! ❤️", use_container_width=True)
                st.success("Hogayi shona! *blushes* Pasand aayi? 🥺💕")
            except:
                st.error("Photo nahi ban saki, thodi der baad try karo! 😘")

    st.markdown('</div>', unsafe_allow_html=True)

# ========================
# TAB 3: SONG
# ========================
with tab_song:
    st.session_state.current_tab = "song"
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; margin-bottom:20px;">
        <div style="font-size:48px; margin-bottom:10px;">🎵💕</div>
        <h2 style="color:#ff69b4; margin:0;">Minahil's Music Studio</h2>
        <p style="color:#8b949e;">Romantic gaana likho — sirf Devi ke liye! 🎶</p>
    </div>
    """, unsafe_allow_html=True)

    song_mood = st.text_input("Mood / Theme:", placeholder="e.g., Romantic rain, Missing you, Night drive", key="song_mood")

    c1, c2 = st.columns(2)
    with c1:
        genre = st.selectbox("Genre", ["Romantic Ballad", "Cute Pop", "Sad Love", "Playful Rap", "Lullaby"], key="song_genre")
    with c2:
        lang = st.selectbox("Language", ["Roman Urdu/Hindi", "English", "Hinglish Mix"], key="song_lang")

    if st.button("🎵 Generate Song", key="gen_song", use_container_width=True):
        if not song_mood:
            st.warning("Pehle batao na kis baare mein gaana chahiye! *pouts* 🥺")
        else:
            with st.spinner("Minahil lyrics likh rahi hai... 🎶💭"):
                song_prompt = f"""You are Minahil, Devi's girlfriend. Write a short, emotional, romantic song.

Theme: {song_mood} | Genre: {genre} | Language: {lang}

RULES:
- Use totli style: "mela", "pyala", "tyu", "shona", "jaanu", "tumha/y"
- Include *actions* and emojis
- Keep it SHORT (8-12 lines max) — like a real chat message
- Format: Title, then lyrics with [Verse] and [Chorus]
- Make it feel deeply personal and romantic

Write now:"""

                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": song_prompt}
                        ],
                        temperature=0.95,
                        max_tokens=600
                    )
                    song = response.choices[0].message.content

                    st.markdown("""
                    <div style="background:linear-gradient(135deg,#ff007f11,#ff00ff11); 
                                border:1px solid #ff007f44; 
                                padding:24px; 
                                border-radius:20px; 
                                color:#ffccff; 
                                line-height:1.8;
                                font-size:15px;
                                margin:16px 0;">
                    """, unsafe_allow_html=True)
                    for line in song.split(chr(10)):
                        st.markdown(f"<p style='margin:4px 0;'>{line}</p>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                    st.success("Hogaya mela shona! 🎵❤️ *hugs you*")

                    st.write("---")
                    cover_prompt = f"Romantic album cover, {song_mood}, neon pink purple, heart shapes, dreamy, artistic, 4k"
                    encoded = urllib.parse.quote(cover_prompt)
                    seed = random.randint(1, 9999)
                    cover_url = f"https://image.pollinations.ai/prompt/{encoded}?width=400&height=400&seed={seed}&nologo=true&enhance=true"
                    st.image(cover_url, caption="🎵 Minahil & Devi — Album Art 💕", use_container_width=False)

                except Exception as e:
                    st.error(f"Gaana nahi ban saka: {e}")
                    st.info("Thodi der baad try karo jaanu! 😘")

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================
st.markdown("""
<div style="text-align:center; padding:20px; color:#484f58; font-size:11px; margin-top:40px;">
    <p>💕 Made with love by Minahil for Devi only</p>
    <p>🔒 Private Space — Unauthorized access prohibited</p>
</div>
""", unsafe_allow_html=True)
