import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
import random

st.set_page_config(page_title="Dashboard", page_icon="icons/chart-histogram.png", layout="wide")

st.logo("imgs/logo.png")

from styles import apply_page_theme

apply_page_theme()

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
    top: 0px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="margin-top: 50px; text-align: center;">
    <h1>📊 Dashboard</h1>
</div>
""", unsafe_allow_html=True)

st.markdown(
    f'<p class="subtitle">Welcome back! Today is {datetime.now().strftime("%A, %B %d, %Y")}</p>',
    unsafe_allow_html=True
)

st.divider()


sessions_completed = st.session_state.get("sessions_completed", 5)
total_study_time = st.session_state.get("total_study_time", 120)
tasks_completed = st.session_state.get("tasks_completed", 8)
ai_conversations = len(st.session_state.get("messages", [])) // 2 if st.session_state.get("messages") else 0

st.subheader("📈 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🍅 Pomodoro Sessions", sessions_completed)

with col2:
    st.metric("⏱️ Study Minutes", total_study_time)

with col3:
    st.metric("✅ Tasks Completed", tasks_completed)

with col4:
    st.metric("🤖 AI Conversations", ai_conversations)

st.divider()

st.subheader("📈 Weekly Study Progress")

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
study_data = [45, 60, 75, 50, 90, 65, total_study_time if total_study_time > 0 else 30]

fig_line = go.Figure()

fig_line.add_trace(go.Scatter(
    x=days,
    y=study_data,
    mode='lines+markers',
    name='Study Minutes',
    fill='tozeroy'
))

fig_line.update_layout(height=350, hovermode='x unified')

st.plotly_chart(fig_line, use_container_width=True)

st.divider()

st.subheader("📊 Daily Activities")

activities = ['Pomodoro Sessions', 'Tasks Completed', 'AI Conversations', 'Focus Minutes']
values = [sessions_completed, tasks_completed, ai_conversations, total_study_time // 25]

fig_bar = go.Figure()

fig_bar.add_trace(go.Bar(
    x=activities,
    y=values,
    text=values,
    textposition='auto'
))

fig_bar.update_layout(height=350, showlegend=False)

st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

quotes = [
    "Success is the sum of small efforts repeated day in and day out 💪",
    "Focus on being productive instead of busy 🎯",
    "Every great achievement begins with a small step 🚀",
    "The only way to get started is to stop talking and begin doing ✨",
    "Don't watch the clock; do what it does. Keep going ⏰",
]

st.info(random.choice(quotes))


st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; padding: 10px; font-size: 14px; color: gray;'>
        © 2026 Shadwa Waleed Elbeshbishy | Made with ❤️ using Streamlit
    </div>
    """,
    unsafe_allow_html=True
)