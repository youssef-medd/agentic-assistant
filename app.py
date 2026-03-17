import streamlit as st
import ollama
from modules.tools import web_search
from modules.parser import process_files

st.set_page_config(page_title="NEXUS — Intelligence Layer", page_icon="◈", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:wght@300;400;500&family=Outfit:wght@300;400;500;600&display=swap');

:root {
  --void: #03040A;
  --surface: #0C0F22;
  --rim: rgba(255,255,255,0.06);
  --rim-strong: rgba(255,255,255,0.12);
  --chrome: #C8D8FF;
  --arc: #4B6EFF;
  --pulse: #00E5C0;
  --text-primary: rgba(255,255,255,0.93);
  --text-secondary: rgba(200,216,255,0.6);
  --text-dim: rgba(200,216,255,0.35);
  --transition: cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes boot {
  0%   { opacity:0; transform:translateY(-12px) scale(0.98); filter:blur(8px); }
  100% { opacity:1; transform:translateY(0) scale(1); filter:blur(0); }
}
@keyframes scan-line {
  0%   { transform:translateY(-100%); }
  100% { transform:translateY(100vh); }
}
@keyframes arc-trace {
  0%,100% { background-position:0% 50%; }
  50%     { background-position:100% 50%; }
}
@keyframes ticker {
  0%,100% { opacity:0.4; }
  50%     { opacity:1; }
}

html, body, [class*="css"] {
  font-family: 'Outfit', sans-serif !important;
  color: var(--text-primary);
  background: var(--void) !important;
}

[data-testid="stAppViewContainer"], .stApp {
  background:
    radial-gradient(ellipse 80% 50% at 10% 0%, rgba(75,110,255,0.12) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 90% 100%, rgba(0,229,192,0.08) 0%, transparent 55%),
    #03040A !important;
}

[data-testid="stAppViewContainer"]::before {
  content: '';
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(75,110,255,0.6), rgba(0,229,192,0.6), transparent);
  animation: scan-line 8s linear infinite;
  pointer-events: none;
  z-index: 9999;
  opacity: 0.4;
}

header[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }

[data-testid="stMain"] { padding: 0 !important; }
.main .block-container {
  max-width: 900px;
  padding: 2.5rem 2rem 6rem !important;
  margin: 0 auto;
}

.nexus-header { animation: boot 1s var(--transition); margin-bottom: 3rem; }
.nexus-eyebrow {
  font-family: 'DM Mono', monospace;
  font-size: 10px;
  letter-spacing: 0.3em;
  color: var(--pulse);
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.nexus-eyebrow::before {
  content: '';
  display: inline-block;
  width: 4px; height: 4px;
  border-radius: 50%;
  background: var(--pulse);
  box-shadow: 0 0 8px var(--pulse);
  animation: ticker 1.5s ease-in-out infinite;
}
.nexus-title {
  font-family: 'Syne', sans-serif;
  font-size: clamp(38px, 5vw, 58px);
  font-weight: 800;
  letter-spacing: -2px;
  line-height: 1;
  background: linear-gradient(135deg, #fff 0%, #C8D8FF 40%, #4B6EFF 75%, #00E5C0 100%);
  background-size: 200% 200%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: arc-trace 6s ease infinite;
  margin-bottom: 8px;
}
.nexus-sub {
  font-family: 'DM Mono', monospace;
  font-size: 12px;
  color: var(--text-secondary);
  letter-spacing: 0.08em;
}

[data-testid="stSidebar"] {
  background: linear-gradient(180deg, rgba(75,110,255,0.08) 0%, transparent 50%), #0C0F22 !important;
  border-right: 1px solid var(--rim) !important;
}
[data-testid="stSidebar"] > div { padding: 1.5rem 1.2rem; }

.sidebar-section-label {
  font-family: 'DM Mono', monospace;
  font-size: 9px;
  letter-spacing: 0.35em;
  text-transform: uppercase;
  color: var(--text-dim);
  margin: 1.5rem 0 0.75rem;
  padding-bottom: 6px;
  border-bottom: 1px solid var(--rim);
}
.status-badge {
  display: flex; align-items: center; gap: 8px;
  padding: 8px 12px; border-radius: 8px;
  background: rgba(0,229,192,0.06);
  border: 1px solid rgba(0,229,192,0.15);
  font-family: 'DM Mono', monospace;
  font-size: 11px; color: var(--pulse); margin-bottom: 6px;
}
.status-badge::before {
  content: '';
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--pulse); box-shadow: 0 0 8px var(--pulse);
  flex-shrink: 0; animation: ticker 2s ease-in-out infinite;
}
.status-badge-info {
  display: flex; align-items: center; gap: 8px;
  padding: 8px 12px; border-radius: 8px;
  background: rgba(75,110,255,0.06);
  border: 1px solid rgba(75,110,255,0.15);
  font-family: 'DM Mono', monospace;
  font-size: 11px; color: var(--chrome);
}

[data-testid="stCheckbox"] {
  padding: 10px 12px !important;
  border-radius: 10px;
  background: rgba(255,255,255,0.025);
  border: 1px solid var(--rim);
  transition: all 0.2s var(--transition);
  margin-bottom: 6px !important;
}
[data-testid="stCheckbox"]:hover {
  background: rgba(75,110,255,0.08);
  border-color: rgba(75,110,255,0.3);
}
[data-testid="stCheckbox"] label {
  font-size: 13px !important; font-weight: 500 !important; color: var(--text-primary) !important;
}
[data-testid="stToggle"] {
  padding: 10px 12px !important; border-radius: 10px;
  background: rgba(255,255,255,0.025); border: 1px solid var(--rim); margin-bottom: 6px !important;
}

[data-testid="stButton"] > button {
  background: transparent !important;
  border: 1px solid var(--rim-strong) !important;
  border-radius: 10px !important;
  color: var(--chrome) !important;
  font-family: 'Syne', sans-serif !important;
  font-size: 13px !important; font-weight: 600 !important;
  letter-spacing: 0.04em !important;
  padding: 0.55rem 1.2rem !important;
  transition: all 0.25s var(--transition) !important;
  width: 100% !important;
}
[data-testid="stButton"] > button:hover {
  border-color: rgba(75,110,255,0.6) !important;
  color: #fff !important;
  box-shadow: 0 0 24px rgba(75,110,255,0.2), inset 0 0 24px rgba(75,110,255,0.05) !important;
  transform: translateY(-1px) !important;
}
[data-testid="stButton"] > button[kind="primary"] {
  background: linear-gradient(135deg, rgba(75,110,255,0.25), rgba(0,229,192,0.12)) !important;
  border-color: rgba(75,110,255,0.5) !important;
}
[data-testid="stButton"] > button[kind="primary"]:hover {
  background: linear-gradient(135deg, rgba(75,110,255,0.4), rgba(0,229,192,0.2)) !important;
  border-color: rgba(75,110,255,0.9) !important;
  box-shadow: 0 0 32px rgba(75,110,255,0.35), 0 0 8px rgba(0,229,192,0.2) !important;
}

[data-testid="stFileUploader"] {
  background: rgba(75,110,255,0.04) !important;
  border: 1px dashed rgba(75,110,255,0.25) !important;
  border-radius: 12px !important;
}
[data-testid="stFileUploader"]:hover {
  background: rgba(75,110,255,0.08) !important;
  border-color: rgba(75,110,255,0.5) !important;
}
[data-testid="stFileUploader"] label {
  color: var(--text-secondary) !important;
  font-size: 12px !important;
  font-family: 'DM Mono', monospace !important;
}

[data-testid="stChatInput"] {
  position: fixed !important;
  bottom: 0 !important; left: 0 !important; right: 0 !important;
  z-index: 1000 !important;
  padding: 1.2rem 2rem !important;
  background: linear-gradient(to top, rgba(3,4,10,0.98) 60%, transparent) !important;
  backdrop-filter: blur(20px) !important;
}
[data-testid="stChatInput"] > div { max-width: 860px; margin: 0 auto; }
[data-testid="stChatInputContainer"] {
  background: #0C0F22 !important;
  border: 1px solid var(--rim-strong) !important;
  border-radius: 16px !important;
  box-shadow: 0 0 0 1px rgba(75,110,255,0.1), 0 8px 40px rgba(3,4,10,0.8), 0 0 60px rgba(75,110,255,0.08) !important;
  transition: all 0.3s var(--transition) !important;
  overflow: hidden;
}
[data-testid="stChatInputContainer"]:focus-within {
  border-color: rgba(75,110,255,0.45) !important;
  box-shadow: 0 0 0 1px rgba(75,110,255,0.3), 0 8px 40px rgba(3,4,10,0.8), 0 0 80px rgba(75,110,255,0.18) !important;
}
[data-testid="stChatInputContainer"] textarea {
  background: transparent !important; border: none !important;
  color: var(--text-primary) !important;
  font-family: 'Outfit', sans-serif !important;
  font-size: 14px !important; caret-color: #4B6EFF !important;
  padding: 1rem 1.2rem !important; resize: none !important;
}
[data-testid="stChatInputContainer"] textarea::placeholder {
  color: var(--text-dim) !important; font-size: 14px !important;
}
[data-testid="stChatInputSubmitButton"] > button {
  background: linear-gradient(135deg, #4B6EFF, rgba(0,229,192,0.7)) !important;
  border: none !important; border-radius: 10px !important;
  padding: 0.5rem 0.9rem !important; margin: 0.4rem !important;
  transition: all 0.2s var(--transition) !important;
}
[data-testid="stChatInputSubmitButton"] > button:hover {
  transform: scale(1.05) !important;
  box-shadow: 0 0 24px rgba(75,110,255,0.5), 0 0 12px rgba(0,229,192,0.3) !important;
}
[data-testid="stChatInputSubmitButton"] > button svg { fill:#fff !important; stroke:#fff !important; }

[data-testid="stExpander"] {
  background: rgba(255,255,255,0.02) !important;
  border: 1px solid var(--rim) !important; border-radius: 12px !important;
}
[data-testid="stExpander"] summary {
  font-family: 'DM Mono', monospace !important;
  font-size: 12px !important; color: var(--text-secondary) !important;
}
[data-testid="stStatus"] {
  background: rgba(75,110,255,0.05) !important;
  border: 1px solid rgba(75,110,255,0.2) !important;
  border-radius: 10px !important;
  font-family: 'DM Mono', monospace !important; font-size: 12px !important;
}
hr { border:none !important; border-top:1px solid var(--rim) !important; margin:1rem 0 !important; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(75,110,255,0.3); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: rgba(75,110,255,0.6); }
</style>
""", unsafe_allow_html=True)


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<div style="margin-bottom:1.5rem;">'
        '<div style="font-family:\'DM Mono\',monospace;font-size:9px;letter-spacing:0.35em;'
        'color:rgba(200,216,255,0.35);text-transform:uppercase;margin-bottom:12px;">NEXUS // v2.4.1</div>'
        '<div style="font-family:\'Syne\',sans-serif;font-size:20px;font-weight:800;'
        'background:linear-gradient(90deg,#fff,#4B6EFF);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">'
        'SYSTEM STATUS</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="status-badge">OLLAMA ENGINE ACTIVE</div>', unsafe_allow_html=True)
    st.markdown('<div class="status-badge-info">&#9672;&nbsp; MODEL · LLAMA 3.2 (3B)</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-label">MODULES</div>', unsafe_allow_html=True)
    enable_web = st.checkbox("◌  Enable Web Search")
    show_debug = st.toggle("Ξ  Debug Extraction", value=False)

    st.markdown('<div class="sidebar-section-label">DOCUMENTS</div>', unsafe_allow_html=True)
    sidebar_files = st.file_uploader(
        "Drop files — PDF / TXT", type=["pdf", "txt"],
        accept_multiple_files=True, label_visibility="visible",
    )

    st.markdown('<div class="sidebar-section-label">CONTROLS</div>', unsafe_allow_html=True)
    if st.button("⌫  Flush Memory", type="primary"):
        st.session_state.messages = []
        st.rerun()


# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="nexus-header">'
    '<div class="nexus-eyebrow">LOCAL INFERENCE · ZERO EGRESS</div>'
    '<div class="nexus-title">NEXUS</div>'
    '<div class="nexus-sub">Document Intelligence Engine &nbsp;·&nbsp; Your data stays on-device</div>'
    '</div>',
    unsafe_allow_html=True,
)


# ─── Session State ────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []


# ─── Custom chat renderer (bypasses Streamlit bubble components entirely) ─────
def render_chat_history(messages):
    if not messages:
        st.markdown(
            '<div style="text-align:center;padding:4rem 0 2rem;'
            'font-family:\'DM Mono\',monospace;font-size:11px;letter-spacing:0.2em;'
            'color:rgba(200,216,255,0.2);">&#9672; &nbsp; AWAITING INPUT</div>',
            unsafe_allow_html=True,
        )
        return

    parts = ['<div style="display:flex;flex-direction:column;">']
    for msg in messages:
        role = msg["role"]
        # Sanitise then preserve line breaks
        safe = (
            msg["content"]
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\n", "<br>")
        )
        if role == "user":
            label      = "YOU"
            lbl_color  = "#4B6EFF"
            bar_color  = "#4B6EFF"
            txt_color  = "rgba(255,255,255,0.95)"
            font_weight = "500"
        else:
            label      = "NEXUS"
            lbl_color  = "#00E5C0"
            bar_color  = "rgba(0,229,192,0.35)"
            txt_color  = "rgba(200,216,255,0.82)"
            font_weight = "400"

        parts.append(
            f'<div style="display:flex;flex-direction:column;padding:1.1rem 0;'
            f'border-top:1px solid rgba(255,255,255,0.04);">'
            f'<span style="font-family:\'DM Mono\',monospace;font-size:9px;'
            f'letter-spacing:0.32em;color:{lbl_color};margin-bottom:8px;'
            f'padding-left:1.1rem;opacity:0.85;">{label}</span>'
            f'<div style="border-left:2px solid {bar_color};padding-left:1.1rem;'
            f'font-family:\'Outfit\',sans-serif;font-size:14.5px;line-height:1.85;'
            f'color:{txt_color};font-weight:{font_weight};">{safe}</div>'
            f'</div>'
        )

    parts.append('</div>')
    st.markdown("".join(parts), unsafe_allow_html=True)


render_chat_history(st.session_state.messages)


# ─── Input ────────────────────────────────────────────────────────────────────
prompt = st.chat_input("Ask anything about your documents...", accept_file="multiple")

if prompt:
    user_text     = prompt.text  if hasattr(prompt, "text")  else prompt
    uploaded_files = prompt.files if hasattr(prompt, "files") else []

    all_files = list(sidebar_files or []) + list(uploaded_files or [])

    context = process_files(all_files) if all_files else ""

    if show_debug and all_files:
        with st.expander("Ξ  Extraction details", expanded=False):
            st.write(f"Files processed: {len(all_files)}")
            st.write(f"Characters extracted: {len(context)}")
            preview = (context[:1500] + ("..." if len(context) > 1500 else "")).strip() or "[empty]"
            st.code(preview)

    if (not user_text or not str(user_text).strip()) and all_files:
        user_text = (
            "Create a professional resume from the uploaded document. "
            "If information is missing, ask me 3–5 targeted questions."
        )

    search_data = ""
    if enable_web and user_text:
        with st.status("◌  Querying web...", expanded=False):
            search_data = web_search(user_text)

    system_instructions = (
        "You are a document QA assistant.\n"
        "ALWAYS answer using only the DOCUMENT CONTEXT plus the USER QUESTION.\n"
        "- If DOCUMENT CONTEXT has no extractable text, explain that clearly.\n"
        "- If DOCUMENT CONTEXT is empty, say you have no text and ask for another file.\n"
        "- If text is present, do NOT say you cannot see the file; just answer from it.\n"
    )
    full_query = (
        f"{system_instructions}\n\n"
        f"DOCUMENT CONTEXT:\n{context}\n\n"
        f"WEB SEARCH RESULTS:\n{search_data}\n\n"
        f"USER QUESTION: {user_text}"
    )

    display_text = user_text if user_text else f"Uploaded {len(all_files)} file(s)."
    st.session_state.messages.append({"role": "user", "content": display_text})

    with st.spinner(""):
        st.markdown(
            '<div style="font-family:\'DM Mono\',monospace;font-size:10px;'
            'letter-spacing:0.25em;color:rgba(0,229,192,0.5);'
            'padding:0.6rem 0 0.4rem 1.1rem;">NEXUS · PROCESSING…</div>',
            unsafe_allow_html=True,
        )
        try:
            history = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages[:-1]
            ]
            history.append({"role": "user", "content": full_query})
            response = ollama.chat(model="llama3.2", messages=history)
            full_response = (
                response.message.content
                if hasattr(response, "message")
                else response["message"]["content"]
            )
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.rerun()
        except Exception as e:
            st.error(f"Engine error: {e}")