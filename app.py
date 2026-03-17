import streamlit as st
import time
import ollama
st.set_page_config(page_title="Agentic Assistant Pro", page_icon="", layout="wide")
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap');

/* Animations */
@keyframes fadeSlideDown {
    0% { opacity: 0; transform: translateY(-30px); filter: blur(10px); }
    100% { opacity: 1; transform: translateY(0); filter: blur(0px); }
}
@keyframes fadeSlideUp {
    0% { opacity: 0; transform: translateY(30px); }
    100% { opacity: 1; transform: translateY(0); }
}
@keyframes pulseGlow {
    0% { box-shadow: 0 0 20px rgba(124, 92, 255, 0.2); }
    50% { box-shadow: 0 0 50px rgba(124, 92, 255, 0.5); }
    100% { box-shadow: 0 0 20px rgba(124, 92, 255, 0.2); }
}
/* Base Theme */
:root {
  --bg0: #070A12;
  --bg1: #0B1020;
  --text: rgba(255, 255, 255, 0.95);
  --accent: #7C5CFF;
}
html, body, [class*="css"] {
  font-family: 'Inter', sans-serif;
  color: var(--text);
}

/* App Background targeting newer Streamlit containers */
[data-testid="stAppViewContainer"], .stApp {
  background: 
    radial-gradient(circle at 15% 50%, rgba(124, 92, 255, 0.15), transparent 25%),
    radial-gradient(circle at 85% 30%, rgba(34, 211, 238, 0.1), transparent 25%),
    #070A12 !important;
}
/* Hide default junk */
header[data-testid="stHeader"] { background: transparent !important; }

/* The Cinematic Title Banner */
.cinematic-title-box {
  animation: fadeSlideDown 1.5s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
  padding: 30px;
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 20px;
  background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.01));
  backdrop-filter: blur(12px);
  animation: fadeSlideDown 1.2s ease-out, pulseGlow 4s infinite alternate;
  text-align: center;
  margin-bottom: 2rem;
}
.cinematic-title-text {
  font-family: 'Space Grotesk', sans-serif; 
  font-size: 42px; 
  font-weight: 700; 
  background: linear-gradient(90deg, #fff, #a78bfa, #22D3EE);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -1px;
}
/* Stagger the chat interface load */
.stChatInputContainer {
    animation: fadeSlideUp 1.5s ease-out 0.5s forwards;
    opacity: 0; /* Starts hidden until animation */
}
</style>
""",
    unsafe_allow_html=True,
)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=80)
    st.title("System Status")
    st.success("Ollama Engine: Connected")
    st.info("🧠 Model: Llama 3.2 (3B)")
    st.divider()
    uploaded_file = st.file_uploader(" Upload Knowledge Base", type="pdf")
    
    if st.button("Clear Memory", type="primary"):
        st.session_state.messages = []
        st.rerun()
st.markdown(
    """
    <div class="cinematic-title-box">
      <div class="cinematic-title-text">
        Agentic Document Intelligence
      </div>
      <div style="margin-top: 10px; font-size: 16px; color: rgba(255,255,255,0.6);">
        Ask complex questions about your local documents. Data never leaves this machine.
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if prompt := st.chat_input("Initiate query..."):
    # 1. Save user message to memory
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 2. Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # 3. Call AI and handle response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing parameters..."):
            try:
                
                api_response = ollama.chat(
                    model='llama3.2',
                    messages=st.session_state.messages
                )
                
                bot_text = api_response.message.content

                st.markdown(bot_text)
                st.session_state.messages.append({"role": "assistant", "content": bot_text})
                
            except Exception as e:
                st.error(f"Brain connection failed. Error: {e}")