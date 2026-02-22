import pandas as pd
import streamlit as st
from datetime import datetime
import json
import os

from styles import apply_page_theme

st.set_page_config(
    page_title="Study Timetable",
    page_icon="icons/calendar-days.png",
    layout="wide",
)

st.logo("imgs/logo.png")


apply_page_theme()

st.markdown("""
<style>
    .main_title {
        text-align: center;
        color: #f5bde6;
        font-size: 3.5em;
        font-weight: 700;
        margin-bottom: 5px;
        text-shadow: 0 0 20px rgba(245, 189, 230, 0.3);
    }
    .sub_title {
        text-align: center;
        color: #8bd5ca;
        font-size: 1.2em;
        margin-bottom: 40px;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        opacity: 0.8;
    }
    .timetable-container {
        max-width: 1200px;
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main_title">📅 Study Timetable</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub_title">Structure and edit your day for maximum productivity</p>', unsafe_allow_html=True)

DATA_FILE = "data/timetable_state.json"
os.makedirs("data", exist_ok=True)

DEFAULT_DATA = {
    "09:00 - 11:00": ["Mathematics", "Physics", "Chemistry", "Biology", "English", "History", "Self Study"],
    "11:00 - 13:00": ["Short Break", "Short Break", "Short Break", "Short Break", "Short Break", "Short Break", "Long Break"],
    "13:00 - 15:00": ["Computer Science", "Mathematics", "Physics", "English Literature", "Organic Chemistry", "Art & Design", "Project Work"],
    "15:00 - 17:00": ["Biology Lab", "History", "Coding Practice", "Advanced Math", "Physics Lab", "English Grammar", "Physical Education"],
    "17:00 - 19:00": ["Daily Review", "Problem Solving", "Free Time", "Journaling", "Reading", "Weak Topics", "Planning"],
}
DAYS = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


if "timetable_df" not in st.session_state:
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                saved_data = json.load(f)
                st.session_state.timetable_df = pd.DataFrame(saved_data, index=DAYS)
        except:
            st.session_state.timetable_df = pd.DataFrame(DEFAULT_DATA, index=DAYS)
    else:
        st.session_state.timetable_df = pd.DataFrame(DEFAULT_DATA, index=DAYS)



st.markdown("### 🛠️ Manage Time Slots")
col_add, col_del = st.columns(2)

with col_add:
    new_col = st.text_input("Add New Time Slot (e.g., 19:00 - 21:00)", placeholder="Add Column Name...")
    if st.button("➕ Add Slot"):
        if new_col and new_col not in st.session_state.timetable_df.columns:
            # Add new column with empty strings
            st.session_state.timetable_df[new_col] = [""] * len(st.session_state.timetable_df)
            st.rerun()
        elif new_col in st.session_state.timetable_df.columns:
            st.warning("This time slot already exists!")

with col_del:
    col_to_delete = st.selectbox("Delete Time Slot", ["Select slot..."] + list(st.session_state.timetable_df.columns))
    if st.button("🗑️ Delete Slot"):
        if col_to_delete != "Select slot...":
            st.session_state.timetable_df = st.session_state.timetable_df.drop(columns=[col_to_delete])
            st.rerun()

st.divider()

st.markdown('<div class="timetable-container">', unsafe_allow_html=True)


st.info("💡 **Tip:** Click on any cell to edit your schedule. You can add more days (rows) using the '+' at the bottom of the table.")


edited_df = st.data_editor(
    st.session_state.timetable_df,
    use_container_width=True,
    num_rows="dynamic",
    key="timetable_editor"
)


col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    if st.button("💾 Save Changes", use_container_width=True, type="primary"):
        st.session_state.timetable_df = edited_df
        with open(DATA_FILE, "w") as f:
            json_data = edited_df.to_dict()
            json.dump(json_data, f)
        st.success("Timetable saved successfully!")
        st.balloons()

st.markdown('</div>', unsafe_allow_html=True)


st.divider()

col1, col2 = st.columns(2)

with col1:
    st.info("### 💡 Tips for Peak Focus")
    st.write("""
    - **Deep Work:** Focus on your hardest subject during your highest energy window.
    - **Active Recall:** Instead of just reading, try to explain concepts from memory.
    - **Hydration:** Keep a water bottle nearby to stay alert.
    """)

with col2:
    st.success("### 🎯 Weekly Goals")
    st.checkbox("Complete 10 Physics problems", value=True)
    st.checkbox("Write English essay draft")
    st.checkbox("Update Biology notes")
    st.checkbox("Review week's progress")



st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; padding: 10px; font-size: 14px; color: gray;'>
        © 2026 Shadwa Waleed Elbeshbishy | Made with ❤️ using Streamlit
    </div>
    """,
    unsafe_allow_html=True
)