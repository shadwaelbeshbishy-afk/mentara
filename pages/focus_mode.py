import streamlit as st

# st.set_page_config(page_title="Focus Mode", layout="wide" , page_icon="icons/bullseye-arrow.png")

from styles import apply_page_theme

# Apply Universal Theme
apply_page_theme()

st.set_page_config(page_title="Focus Mode", page_icon="icons/bullseye-arrow.png", layout="wide")

st.logo("imgs/logo.png")





st.markdown("""
<style>
    .stAudio {
        display: none;
        height: 0;
        overflow: hidden;
    }
    .stTextInput input {
        color: #ffffff;
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .stToggle {
        margin-bottom: 10px;
    }
    /* Button center and specialized style */
    div.stButton > button {
        background: linear-gradient(135deg, #6215EA 0%, #0068ff 100%);
        color: white;
        padding: 12px 28px;
        border-radius: 30px;
        border: none;
        font-size: 18px;
        font-weight: 600;
        transition: 0.3s ease;
        width: auto;
        min-width: 200px;
        display: block;
        margin: 0 auto;
    }
    div.stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(98, 21, 234, 0.4);
    }

        .subtitle {
    text-align: center;
    color: #8bd5ca;
    font-size: 1.2em;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    opacity: 0.8;
    position: relative;
    top: 0px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="margin-top: 50px; text-align: center;">
    <h1>🎯 Focus Mode</h1>
</div>
""", unsafe_allow_html=True)


st.markdown('<p class="subtitle">Get in the zone and crush your goals.</p>', unsafe_allow_html=True)

st.divider()

goal = st.text_input("What is your goal?" , placeholder="Enter your goal")

if goal:
    st.write("Your goal is: ", goal)

st.divider()

st.markdown("""

### 🎵 Focus Music

""")

col1, col2, col3 , col4 = st.columns(4)

with col1:
    lofi = st.toggle(" 🎧 Lofi")
with col2:
    nature = st.toggle(" 🌳 Nature")
with col3:
    ocean = st.toggle(" 🌊 Ocean")
with col4:
    piano = st.toggle(" 🎹 Piano")
    

if lofi:
    st.audio("sounds/lofi.mp3", autoplay=True)
if nature:
    st.audio("sounds/nature.mp3", autoplay=True)
if ocean:
    st.audio("sounds/ocean.mp3", autoplay=True)
if piano:
    st.audio("sounds/piano.mp3", autoplay=True)

st.markdown("<div class='st.my-divider'></div>", unsafe_allow_html=True)



st.markdown(
"<hr style='margin: 2em 0px; padding-top: 10px;color: #faeaff;background-color: transparent;border-top: none;border-right: none;border-left: none;border-image: initial;border-bottom: 1px solid rgba(250, 250, 250, 0.2);' />",
    unsafe_allow_html=True
)



st.markdown(
    "<h1>🎯 Focus Tips</h1>",
    unsafe_allow_html=True
)



tips = [
    "🧹 Keep your space clean",
    "📵 Put your phone away",
    "🎯 Set clear, small goals",
    "🎧 Study with instrumental music",
    "💧 Drink water & move a little",
    "✍️ Study actively (write & explain)",
    "😴 Sleep well & keep a routine",
]


st.markdown("### ✅ Focus Tips")

for tip in tips:
    st.markdown(f"- {tip}")

import streamlit as st

st.markdown("""
<style>
div.stButton > button {
    background-color: #6215EA;
    color: white;
    padding: 12px 28px;
    border-radius: 30px;
    border: none;
    font-size: 18px;
    font-weight: 600;
    transition: 0.3s ease;
    width: 300px;
}

div.stButton > button:hover {
    background-color: #0068ff;
    transform: scale(1.05);
}

div.stButton > button:active {
    transform: scale(0.98);
}
</style>
""", unsafe_allow_html=True)

if st.button("✅ Done!"):
    st.balloons()
    st.markdown(
        "<h3 style='text-align:center;'>🎉 You have completed your focus mode</h3>",
        unsafe_allow_html=True
    )


st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; padding: 10px; font-size: 14px; color: gray;'>
        © 2026 Shadwa Waleed Elbeshbishy | Made with ❤️ using Streamlit
    </div>
    """,
    unsafe_allow_html=True
)