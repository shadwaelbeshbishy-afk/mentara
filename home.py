import streamlit as st
from datetime import datetime
import random
import json
import requests
import os
from pathlib import Path
from zoneinfo import ZoneInfo
from styles import apply_page_theme

st.set_page_config(
    page_title="Home page",
    page_icon="icons/house-chimney.png",
    layout="wide",
)


apply_page_theme()

st.markdown("""
<style>
    .title {
        text-align: center;
        color: #fff;
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #fff;
        font-size: 1.2em;
        margin-bottom: 40px;
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        opacity: 0.8;
    }
    .quote-box {
        background: rgba(227, 228, 233, 0.2);
        padding: 30px;
        border-radius: 20px;
        margin: 20px 0;
        border-left: 5px solid #f5bde6;
    }
    .stImage {
        height: 250px;
        width: 600px;
        position: relative;
        left: 230px;
        top: -100px;
        padding-bottom: 0px;
    }

    .sub_title {
        text-align: center;
        color: #8bd5ca;
        font-size: 1.2em;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        opacity: 0.8;
        position: relative;
        top: -130px;
    }

    .greeting_sub {
        color: #8bd5ca;
        font-size: 1.2em;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        opacity: 0.8;
    }

""", unsafe_allow_html=True)



base_dir = Path(__file__).parent
logo_path = base_dir / "imgs" / "logo.png"

if logo_path.exists():
    st.image(str(logo_path))
    st.logo(str(logo_path))
else:
    st.error(f"Logo file not found at {logo_path}. Please check if 'imgs/logo.png' exists.")



st.markdown('<p class="sub_title">Proven methods to learn faster and remember longer.</p>', unsafe_allow_html=True)


egypt_tz = ZoneInfo("Africa/Cairo")
now_egypt = datetime.now(egypt_tz)
hour = now_egypt.hour

if 5 <= hour < 12:
    greeting = "Good Morning ☀️"
elif 12 <= hour < 18:
    greeting = "Good Afternoon 🌤️"
else:
    greeting = "Good Evening 🌙"




col1,col2,col3=st.columns(3)

with col1:
    st.markdown(f"<h2>{greeting}</h2>", unsafe_allow_html=True)


with col2:
    st.markdown(f"### 📅{now_egypt.strftime('%A-%B-%d-%Y')}")

with col3:
    st.markdown(f"### ⏰{now_egypt.strftime('%I:%M %p')}")




try:
    with open("data/quotes.json", "r") as f:
        quotes=json.load(f)
        quote=random.choice(quotes)
    st.markdown(
        f"""
        <div class="quote-box">
            <div style="font-style: italic; font-family: 'Times New Roman', Times, serif; font-size: 1.5em; color: #fff; margin-bottom: 10px; text-align: center;">
                "{quote['quote']}"
            </div>
            <div style="font-weight: bold; font-size: 1.2em; font-family: 'Times New Roman', Times, serif; color: #fff; text-align: center;">
                — {quote['author']}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


except Exception:
    st.markdown("### 🗒️  could not load quotes ")

st.divider()

col1,col2,col3,col4=st.columns(4)
with col1:
    st.metric("### ⏱ Study Time", "00:00:00")
with col2:
    st.metric("### 🎯 Goal completion", "0%")
with col3:
    st.metric("### 📖 Daily Words", "0")
with col4:
    st.metric("### 🔥 Streak", "0")


st.divider()

st.markdown("### ✨ features")

col1,col2,col3,col4=st.columns(4)
with col1:
    st.markdown("""
    ### 🤖 AI Assistant
    helps you to understand concepts, not just get answers.
    """)

with col2:
    st.markdown("""
    ### 🎯 Focus Mode
    helps you to focus on your studies and take breaks.
    """)

with col3:
    st.markdown("""
    ### 📆Timetable
    Helps you organize your time.
    """)

with col4:
    st.markdown("""
    ### ⏱️Pomodoro
    helps you to focus on your studies and take breaks.
    """)


col5,col6,col7,col8=st.columns(4)
with col5:
    st.markdown("""
    ### 📝 Note taking
    helps you to take notes for your subjects.
    """)
with col6:
    st.markdown("""
    ### 🧠 Techniques
    helps you to learn new things and improve your memory.
    """)
with col7:
    st.markdown("""
    ### 📊 Dashboard
    helps you to track your progress and stay motivated.
    """)
with col8:
    st.markdown("""
    ### 📖 Daily Words
    helps you to learn new words and improve your vocabulary.
    """)

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; padding: 10px; font-size: 14px; color: gray;'>
        © 2026 Shadwa Waleed Elbeshbishy | Made with ❤️ using Streamlit
    </div>
    """,
    unsafe_allow_html=True
)