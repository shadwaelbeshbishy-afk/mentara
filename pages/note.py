import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="Notes", page_icon="icons/journal-alt.png", layout="wide")

from styles import apply_page_theme

apply_page_theme()

st.logo("imgs/logo.png")


st.markdown("""
<style>
    .stTextInput input, .stTextArea textarea {
        color: #ffffff;
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)
st.markdown("""
<div style="margin-top: 30px; text-align: center; font-size: 40px;">
    <h1>📝 My Study Notes</h1>
</div>
""", unsafe_allow_html=True)



DATA_FILE = "data/notes.json"

if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

def load_notes():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_notes(notes):
    with open(DATA_FILE, "w") as f:
        json.dump(notes, f, indent=4)

notes = load_notes()

st.subheader("✍️ Create a New Note")

title = st.text_input("Note Title")
subject = st.selectbox(
    "Subject",
    ["General", "Math", "Science", "English", "History", "Programming"]
)
tags = st.text_input("Tags (comma separated)")
content = st.text_area("Write your note here...", height=250)

if st.button("💾 Save Note"):
    if title and content:
        new_note = {
            "title": title,
            "subject": subject,
            "tags": [tag.strip() for tag in tags.split(",") if tag.strip()],
            "content": content,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        notes.append(new_note)
        save_notes(notes)
        st.success("Note saved successfully!")
        st.rerun()
    else:
        st.warning("Title and content cannot be empty.")

st.divider()

st.subheader("📚 Your Saved Notes")

if not notes:
    st.info("No notes yet. Start writing one above!")
else:
    for i, note in enumerate(notes):
        with st.expander(f"📌 {note['title']} ({note['subject']})"):
            st.markdown(f"**🗓 Date:** {note['date']}")
            st.markdown(f"**🏷 Tags:** {', '.join(note['tags']) if note['tags'] else 'None'}")
            st.markdown("---")
            st.write(note["content"])

            if st.button("🗑 Delete", key=f"delete_{i}"):
                notes.pop(i)
                save_notes(notes)
                st.success("Note deleted.")
                st.rerun()


st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; padding: 10px; font-size: 14px; color: gray;'>
        © 2026 Shadwa Waleed Elbeshbishy | Made with ❤️ using Streamlit
    </div>
    """,
    unsafe_allow_html=True
)