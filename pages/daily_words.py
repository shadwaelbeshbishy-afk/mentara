import streamlit as st
import random
import json
import os
from datetime import datetime
from styles import apply_page_theme

st.set_page_config(page_title="Daily Words", page_icon="icons/book-brain.png", layout="wide")

st.logo("imgs/logo.png")


st.markdown("""
<style>
.subtitle {
    text-align: center;
    color: #8bd5ca;
    font-size: 1.2em;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    opacity: 0.8;
    position: relative;
    top: 160px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="subtitle">Expand your vocabulary, one word at a time.</p>', unsafe_allow_html=True)



apply_page_theme()

VOCAB_FILE = "data/vocab.json"

def load_vocabulary(path):
    if not os.path.exists(path):
        return []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("vocabulary", [])
    except Exception:
        return []

def get_daily_word(words):
    if not words:
        return None
    day_of_year = datetime.now().timetuple().tm_yday
    random.seed(day_of_year)
    word = random.choice(words)
    random.seed() 
    return word

def init_state(key, default):
    if key not in st.session_state:
        st.session_state[key] = default

init_state("saved_words", [])
init_state("quiz_word", None)

@st.cache_data
def get_words():
    return load_vocabulary(VOCAB_FILE)

words = get_words()
if not words:
    st.error("No words found in data/vocab.json")
    st.stop()

st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1 style="font-size: 3rem; margin-bottom: 0; margin-top: 10px;">📖 Daily Words</h1>
    </div>
""", unsafe_allow_html=True)







st.divider()

daily_word = get_daily_word(words)

col_daily, col_library = st.columns([2, 1], gap="large")

with col_daily:
    st.subheader("🌟 Today's Selection")

    with st.container(border=True):
        st.markdown(f"""
            <div style="padding: 20px; text-align: center;">
                <h1 style="color: #8bd5ca; font-size: 4rem; margin: 0;">{daily_word["word"]}</h1>
                <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.1); margin: 20px 0;">
                <h3 style="margin-bottom: 10px;">Definition</h3>
                <p style="font-size: 1.3rem; opacity: 0.9;">{daily_word["definition"]}</p>
                <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; margin-top: 20px;">
                    <i style="opacity: 0.7;">Example: "{daily_word["example"]}"</i>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("❤️ Save to Library", use_container_width=True):
            if daily_word not in st.session_state.saved_words:
                st.session_state.saved_words.append(daily_word)
                st.toast("Saved to your library!", icon="✅")
            else:
                st.toast("Already in your library.", icon="ℹ️")

    st.divider()

    st.subheader("🔍 Explore Others")

    others = [w for w in words if w != daily_word]
    sample = random.sample(others, min(4, len(others)))

    c1, c2 = st.columns(2)
    for i, word in enumerate(sample):
        col = c1 if i % 2 == 0 else c2
        with col:
            with st.expander(f"📌 {word['word']}"):
                st.write(word["definition"])
                st.write(f"*Example: {word['example']}*")
                if st.button("Save", key=f"save_{word['word']}"):
                    if word not in st.session_state.saved_words:
                        st.session_state.saved_words.append(word)
                        st.toast(f"Saved {word['word']}!", icon="✅")
                    else:
                        st.toast("Already saved.", icon="ℹ️")

with col_library:
    st.subheader("📚 My Library")

    saved = st.session_state.saved_words

    if not saved:
        st.info("No saved words yet. Start building your vocabulary!")
    else:
        for i, word in enumerate(saved):
            with st.expander(f"📖 {word['word']}"):
                st.write(word["definition"])
                if st.button("🗑️ Remove", key=f"del_{i}"):
                    saved.pop(i)
                    st.rerun()

    st.divider()

    st.subheader("🎯 Quick Quiz")

    if len(saved) < 1:
        st.warning("Save at least one word to unlock the quiz!")
    else:
        if st.button("🎲 Get Random Question", type="primary", use_container_width=True):
            st.session_state.quiz_word = random.choice(saved)
            st.rerun()

        if st.session_state.quiz_word:
            q_word = st.session_state.quiz_word
            st.markdown(f"**What word means:**")
            st.info(f"*{q_word['definition']}*")

            user_ans = st.text_input("Type your answer:", key="quiz_input")

            if st.button("Check Answer", use_container_width=True):
                if user_ans.lower().strip() == q_word["word"].lower().strip():
                    st.balloons()
                    st.success(f"✨ Correct! The word is **{q_word['word']}**.")
                else:
                    st.error(f"❌ Not quite. The correct word is **{q_word['word']}**.")


st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; padding: 10px; font-size: 14px; color: gray;'>
        © 2026 Shadwa Waleed Elbeshbishy | Made with ❤️ using Streamlit
    </div>
    """,
    unsafe_allow_html=True
)