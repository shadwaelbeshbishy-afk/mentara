import streamlit as st
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from styles import apply_page_theme
from helpers import load_json


st.logo("imgs/logo.png")


st.markdown("""
<style>
    .sub_title {
        text-align: center;
        color: #8bd5ca;
        font-size: 1.2em;
        margin-bottom: 40px;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        opacity: 0.8;
    }
</style>
""", unsafe_allow_html=True)



st.set_page_config(page_title="Study Techniques", page_icon="icons/wisdom.png", layout="wide")
apply_page_theme()



@st.cache_data
def load_techniques():
    return load_json("data/study_techniques.json", default=[])

techs = load_techniques()

st.markdown("""
<div style="margin-top: 50px; text-align: center;">
    <h1>🧠 Study Techniques</h1>
</div>
""", unsafe_allow_html=True)
st.markdown('<p class="sub_title">Proven methods to learn faster and remember longer.</p>', unsafe_allow_html=True)

st.divider()

if not techs:
    st.error("No techniques found. Check data/study_techniques.json")
    st.stop()

for t in techs:
    with st.expander(f"{t.get('emoji', '📘')}  {t.get('name', 'Technique')}"):

        col_txt, col_vid = st.columns([3, 2], gap="large")

        with col_txt:
            st.markdown(f"**{t.get('description', t.get('why_it_works', 'No description available.'))}**")
            st.markdown("")

            st.markdown("#### 💡 Why It Works")
            st.info(t.get("why_it_works", "Scientific explanation coming soon."))

            if "best_subjects" in t:
                st.markdown("#### 📚 Best Subjects")
                st.markdown(" · ".join(f"`{s}`" for s in t["best_subjects"]))

            if "steps" in t:
                st.markdown("#### 📝 How To Do It")
                for i, step in enumerate(t["steps"], 1):
                    st.markdown(f"{i}. {step}")

        with col_vid:
            st.markdown("#### 🎬 Watch & Learn")
            video_url = t.get("link")
            if video_url:
                st.video(video_url)
            else:
                st.info("Video tutorial coming soon! Stay tuned.")


st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; padding: 10px; font-size: 14px; color: gray;'>
        © 2026 Shadwa Waleed Elbeshbishy | Made with ❤️ using Streamlit
    </div>
    """,
    unsafe_allow_html=True
)