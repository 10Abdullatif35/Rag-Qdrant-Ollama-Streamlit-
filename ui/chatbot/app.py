import sys, json
from pathlib import Path
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.rag.rag_chain import get_rag_response
from src.embeddings.embedder import get_embedding
from src.rag.retriever import get_top_chunks

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Etiya Chatbot", layout="wide", initial_sidebar_state="collapsed")
css = Path(__file__).with_name("style.css").read_text()
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# ---- SESSION STATE ----
if "chat" not in st.session_state:
    st.session_state.chat = [
        {"role":"bot","text":"Merhaba! Size nasıl yardımcı olabilirim?"}
    ]
if "open" not in st.session_state:
    st.session_state.open = False

# ---- FLOATING ICON (always rendered) ----
st.markdown("""
<div id="chat-fab" onclick="toggleChat()">💬</div>
<script>
function toggleChat(){
  const win = parent.document.getElementById('chat-window');
  if(!win) return;
  if(win.style.display==='flex'){win.style.display='none';}
  else{win.style.display='flex';}
}
</script>
""", unsafe_allow_html=True)

# ---- CHAT WINDOW ----
st.markdown('<div id="chat-window">', unsafe_allow_html=True)
st.markdown('<div id="chat-header">Etiya Asistan</div>', unsafe_allow_html=True)
st.markdown('<div id="chat-body">', unsafe_allow_html=True)

for msg in st.session_state.chat:
    cls = "bot-msg" if msg["role"]=="bot" else "user-msg"
    st.markdown(f'<div class="{cls}">{msg["text"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)   # chat-body close

# ---- INPUT BOX ----
user_input = st.chat_input("Merhaba size nasıl yardımcı olablirim?")  # Enter ile gönder, sonra temizlenir
if user_input:
    st.session_state.chat.append({"role": "user", "text": user_input})
    answer = get_rag_response(user_input, top_k=5)
    st.session_state.chat.append({"role": "bot", "text": answer})
    st.rerun()

