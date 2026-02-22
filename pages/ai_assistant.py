import streamlit as st
import google.generativeai as genai
import PyPDF2

from styles import apply_page_theme

st.set_page_config(page_title="Personal AI", page_icon="icons/user-robot.png", layout="wide")

apply_page_theme()

st.logo("imgs/logo.png")


st.markdown("""
<style>

    .stButton button { 
        border-radius: 12px;
        width: 100%;
        padding: 12px 20px;
        font-size: 15px;
        font-weight: 500;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(138, 43, 226, 0.3);
        border-color: rgba(138, 43, 226, 0.5);
    }

    .stChatInputContainer { 
        padding-bottom: 20px;
        padding-top: 10px;
    }
    
    button[data-testid="baseButton-secondary"] {
        border-radius: 50%;
        width: 45px;
        height: 45px;
        font-size: 20px;
        padding: 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        transition: all 0.3s ease;
    }
    
    button[data-testid="baseButton-secondary"]:hover {
        transform: scale(1.1);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    h1 {
        background: linear-gradient(135deg, #8bd5ca 0%, #8bd5ca 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 30px;
    }
    
    .stChatMessage {
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)


genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')
if "messages" not in st.session_state:
    st.session_state.messages = []
if "context" not in st.session_state:
    st.session_state.context = ""

st.title("Hi! I'm your study buddy, how can I help you today?")

# if not st.session_state.messages:
#     st.markdown("### 💡 Quick Suggestions")
    
    # SUGGESTIONS = {
    #     "💡 Study Hacks": "Give me some effective study hacks for better focus.",
    #     "🧠 Memory Power": "How can I improve my long-term memory for exams?",
    #     "📈 Grade Boost": "What's the best way to organize my study schedule to improve grades?",
    #     "🎯 Concentration": "Suggest some techniques to improve deep work concentration."
    # }
    
    # col1, col2 = st.columns(2)
    # with col1:
    #     if st.button("💡 Study Hacks", use_container_width=True):
    #         prompt = SUGGESTIONS["💡 Study Hacks"]
    #         st.session_state.messages.append({"role": "user", "content": prompt})
    #         with st.spinner("Thinking..."):
    #             response = model.generate_content(prompt)
    #             st.session_state.messages.append({"role": "assistant", "content": response.text})
    #         st.rerun()
    #     if st.button("📈 Grade Boost", use_container_width=True):
    #         prompt = SUGGESTIONS["📈 Grade Boost"]
    #         st.session_state.messages.append({"role": "user", "content": prompt})
    #         with st.spinner("Thinking..."):
    #             response = model.generate_content(prompt)
    #             st.session_state.messages.append({"role": "assistant", "content": response.text})
    #         st.rerun()
    # with col2:
    #     if st.button("🧠 Memory Power", use_container_width=True):
    #         prompt = SUGGESTIONS["🧠 Memory Power"]
    #         st.session_state.messages.append({"role": "user", "content": prompt})
    #         with st.spinner("Thinking..."):
    #             response = model.generate_content(prompt)
    #             st.session_state.messages.append({"role": "assistant", "content": response.text})
    #         st.rerun()
    #     if st.button("🎯 Concentration", use_container_width=True):
    #         prompt = SUGGESTIONS["🎯 Concentration"]
    #         st.session_state.messages.append({"role": "user", "content": prompt})
    #         with st.spinner("Thinking..."):
    #             response = model.generate_content(prompt)
    #             st.session_state.messages.append({"role": "assistant", "content": response.text})
    #         st.rerun()
    
st.markdown("---")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

st.markdown("<br>", unsafe_allow_html=True)


with st.popover("➕ Upload Study Material", help="Upload PDF or Text files"):
    st.markdown("**📎 Upload File**")
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt"], label_visibility="collapsed")
    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            st.session_state.context = "" 
            for page in reader.pages:
                st.session_state.context += page.extract_text() or ""
            st.success(f"✅ PDF loaded! ({len(reader.pages)} pages)")
        elif uploaded_file.type == "text/plain":
            st.session_state.context = uploaded_file.read().decode("utf-8")
            st.success("✅ Text file loaded!")
    
    if st.session_state.context:
        st.info(f"📄 Context: {len(st.session_state.context)} characters")
        if st.button("🗑️ Clear Context"):
            st.session_state.context = ""
            st.rerun()

if prompt := st.chat_input("Ask me anything about your studies..."):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            full_prompt = f"Context: {st.session_state.context}\n\nQuestion: {prompt}" if st.session_state.context else prompt
            response = model.generate_content(full_prompt)
            st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
