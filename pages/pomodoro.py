import streamlit as st
import time
import datetime
import streamlit.components.v1 as components
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



st.logo("imgs/logo.png")





from styles import apply_page_theme

apply_page_theme()

st.set_page_config(page_title="Pomodoro", page_icon="icons/alarm-clock.png", layout="wide")


st.markdown("""
<style>
    /* Title Styling */
    .pomodoro-title {
        text-align: center;
        color: white;
        font-family: 'Poppins', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }   
    .timer-card {
        background-color: rgba(227, 228, 233, 0.5);
        backdrop-filter: blur(5px);
        border-radius: 25px;
        padding: 40px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        margin: 20px auto;
        max-width: 600px;
    }
    /* Progress Bar */
    .progress-container {
        width: 100%;
        height: 20px;
        background-color: rgba(227, 228, 233, 0.5);
        border-radius: 10px;            
        overflow: hidden;
        margin: 20px 0;
    }
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #667eea, #764ba2);
        transition: width 1s linear;
        border-radius: 10px;
    }
    /* Buttons */
    .stButton button {
        width: 100%;
        padding: 15px 30px;
        font-size: 1.2rem;
        font-weight: 600;
        border-radius: 15px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }
    /* Number Input */
    .stNumberInput input {
        font-size: 1.1rem;
        padding: 12px;
        border-radius: 10px;
        border: 2px solid rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    .stNumberInput input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    /* Stats Card */
    .stats-card {
        background-color: rgba(227, 228, 233, 0.5);
        backdrop-filter: blur(5px);
        border-radius: 20px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: transform 0.3s ease;
    }
    .stats-card:hover { transform: translateY(-5px); }
    .stat-number {
        font-size: 2.2rem;
        font-weight: 700;
        color: #41138C;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .stat-label {
        font-size: 0.9rem;
        color: #fff;
        text-transform: uppercase;
        letter-spacing: 1px;
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


def request_notification_permission():

    components.html("""
    <script>
        if ('Notification' in window && Notification.permission === 'default') {
            Notification.requestPermission();
        }
    </script>
    """, height=0)

def send_notification(title, body, icon="🍅"):

    components.html(f"""
    <script>
        if ('Notification' in window && Notification.permission === 'granted') {{
            new Notification('{title}', {{
                body: '{body}',
                icon: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y="0.9em" font-size="90">{icon}</text></svg>',
                requireInteraction: true,
                vibrate: [200, 100, 200]
            }});
        }}
    </script>
    """, height=0)

def show_popup(title, message, emoji, button_text, gradient_colors):

    components.html(f"""
    <style>
        @keyframes slideDown {{
            from {{ transform: translateY(-100%); opacity: 0; }}
            to {{ transform: translateY(0); opacity: 1; }}
        }}
        
        @keyframes confetti {{
            0% {{ transform: translateY(0) rotate(0deg); opacity: 1; }}
            100% {{ transform: translateY(100vh) rotate(720deg); opacity: 0; }}
        }}
        
        .popup-overlay {{
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.85);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
        }}
        
        .popup-content {{
            background: linear-gradient(135deg, {gradient_colors});
            padding: 50px 70px;
            border-radius: 25px;
            text-align: center;
            box-shadow: 0 25px 70px rgba(0, 0, 0, 0.6);
            animation: slideDown 0.6s ease;
            max-width: 550px;
        }}
        
        .popup-content h1 {{
            color: white;
            font-size: 3.5rem;
            margin: 0 0 20px 0;
            font-family: 'Poppins', sans-serif;
        }}
        
        .popup-content p {{
            color: white;
            font-size: 1.4rem;
            margin: 0 0 35px 0;
            line-height: 1.6;
        }}
        
        .popup-button {{
            background: white;
            color: {gradient_colors.split(',')[0]};
            border: none;
            padding: 18px 45px;
            border-radius: 30px;
            font-size: 1.2rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .popup-button:hover {{
            transform: scale(1.1);
            box-shadow: 0 8px 25px rgba(255, 255, 255, 0.4);
        }}
        
        .confetti {{
            position: fixed;
            width: 12px;
            height: 12px;
            animation: confetti 4s linear;
        }}
    </style>
    
    <div class="popup-overlay" id="popup">
        <div class="popup-content">
            <h1>{emoji} {title}</h1>
            <p>{message}</p>
            <button class="popup-button" onclick="closePopup()">{button_text}</button>
        </div>
    </div>
    
    <script>
        // Create confetti
        for (let i = 0; i < 60; i++) {{
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            confetti.style.left = Math.random() * 100 + '%';
            confetti.style.top = -10 + 'px';
            confetti.style.backgroundColor = ['#FFD700', '#FF69B4', '#00CED1', '#7FFF00', '#FF4500', '#9370DB'][Math.floor(Math.random() * 6)];
            confetti.style.animationDelay = Math.random() * 2 + 's';
            document.getElementById('popup').appendChild(confetti);
        }}
        
        function closePopup() {{
            document.getElementById('popup').style.display = 'none';
        }}
        
        // Play celebration sound
        const audio = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBSuBzvLZiTYIGWi77eifTRAMUKfj8LZjHAY4ktjyzHksBSR3x/DdkUAKFF606+upVRQKRp/g8r5sIQUrgs/y2Yk2CBlou+3on00QDFC');
        audio.play().catch(e => console.log('Audio failed'));
    </script>
    """, height=650)


if "running" not in st.session_state:
    st.session_state.running = False
if "paused" not in st.session_state:
    st.session_state.paused = False
if "current_phase" not in st.session_state:
    st.session_state.current_phase = "study"  
if "sessions_completed" not in st.session_state:
    st.session_state.sessions_completed = 0
if "total_study_time" not in st.session_state:
    st.session_state.total_study_time = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = None



st.markdown('<h1 class="pomodoro-title">🍅 Pomodoro Timer</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Stay focused, work smart, achieve more</p>', unsafe_allow_html=True)



col_stat1, col_stat2, col_stat3 = st.columns(3)

with col_stat1:
    st.markdown(f"""
    <div class="stats-card" style="text-align: center;">
        <div class="stat-number">{st.session_state.sessions_completed}</div>
        <div class="stat-label">Sessions</div>
    </div>
    """, unsafe_allow_html=True)

with col_stat2:
    st.markdown(f"""
    <div class="stats-card" style="text-align: center;">
        <div class="stat-number">{st.session_state.total_study_time}</div>
        <div class="stat-label">Minutes Studied</div>
    </div>
    """, unsafe_allow_html=True)

with col_stat3:
    current_time = datetime.datetime.now().strftime("%H:%M")
    st.markdown(f"""
    <div class="stats-card" style="text-align: center;">
        <div class="stat-number">{current_time}</div>
        <div class="stat-label">Current Time</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


st.markdown("### ⚙️ Timer Settings")

col1, col2 = st.columns(2)
with col1:
    session_mins = st.number_input("📚 Study Duration (minutes)", value=25, min_value=1, max_value=120, key="study_mins")
with col2:
    break_mins = st.number_input("☕ Break Duration (minutes)", value=5, min_value=1, max_value=30, key="break_mins")

st.markdown("<br>", unsafe_allow_html=True)


col_start, col_pause, col_stop, col_reset = st.columns(4)

with col_start:
    if st.button("▶️ Start", disabled=st.session_state.running and not st.session_state.paused, use_container_width=True):
        st.session_state.running = True
        st.session_state.paused = False
        st.session_state.start_time = time.time()

with col_pause:
    if st.button("⏸️ Pause", disabled=not st.session_state.running or st.session_state.paused, use_container_width=True):
        st.session_state.paused = True

with col_stop:
    if st.button("⏹️ Stop", disabled=not st.session_state.running, use_container_width=True):
        st.session_state.running = False
        st.session_state.paused = False
        st.session_state.current_phase = "study"

with col_reset:
    if st.button("🔄 Reset Stats", use_container_width=True):
        st.session_state.sessions_completed = 0
        st.session_state.total_study_time = 0
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)


if st.session_state.running and not st.session_state.paused:

    if st.session_state.current_phase == "study":
        total_seconds = session_mins * 60
        phase_name = "✍️ Study Time"
        phase_color = "#667eea"
    else:
        total_seconds = break_mins * 60
        phase_name = "☕ Break Time"
        phase_color = "#ff6b6b"
    
    st.markdown(f"### {phase_name}")
    
    
    timer_placeholder = st.empty()
    progress_placeholder = st.empty()
    
    remaining_time = total_seconds
    
    while remaining_time > 0 and st.session_state.running and not st.session_state.paused:
        mins, secs = divmod(remaining_time, 60)
        
        
        progress = ((total_seconds - remaining_time) / total_seconds) * 100
        
        
        timer_placeholder.markdown(
            f"""
            <div style="text-align: center; padding: 30px; background: rgba(255,255,255,0.95); border-radius: 20px; margin: 20px 0;">
                <h1 style="font-size: 6rem; margin: 0; color: {phase_color}; font-family: 'Courier New', monospace;">
                    {mins:02d}:{secs:02d}
                </h1>
            </div>
            """,
            unsafe_allow_html=True
        )
        

        progress_placeholder.markdown(
            f"""
            <div class="progress-container">
                <div class="progress-bar" style="width: {progress}%; background: {phase_color};"></div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        time.sleep(1)
        remaining_time -= 1
    
    
    if remaining_time == 0 and st.session_state.running:
        if st.session_state.current_phase == "study":
            
            st.session_state.sessions_completed += 1
            st.session_state.total_study_time += session_mins
            
            
            if "user_id" in st.session_state:
                db.update_user_stats(
                    user_id=st.session_state.user_id,
                    sessions=1,
                    study_time=session_mins,
                    tasks=0
                )
            
            send_notification(
                "🎉 Study Session Complete!",
                f"Great work! You studied for {session_mins} minutes.",
                "🎉"
            )
            
            show_popup(
                "Study Complete!",
                f"Excellent work! You've completed a {session_mins}-minute study session.<br>Time for a well-deserved break!",
                "🎉",
                "Start Break ☕",
                "#667eea 0%, #764ba2 100%"
            )
            
            
            st.session_state.current_phase = "break"
            st.rerun()
            
        else:
            
            send_notification(
                "⏰ Break Time Over!",
                f"Your {break_mins} minute break is done. Ready for another session?",
                "⏰"
            )
            
            show_popup(
                "Break Over!",
                f"Your {break_mins}-minute break is complete.<br>Ready to crush another study session?",
                "⏰",
                "Let's Go! 🚀",
                "#ff4b4b 0%, #ff6b6b 100%"
            )
            
            
            st.session_state.current_phase = "study"
            st.session_state.running = False
            st.rerun()

elif st.session_state.paused:
    st.info("⏸️ Timer paused. Click 'Start' to resume.")
else:
    st.markdown("""
    <div style="text-align: center; padding: 50px; background: rgba(255,255,255,0.9); border-radius: 20px; margin: 20px 0;">
        <h2 style="color: #667eea; margin-bottom: 15px;">Ready to focus?</h2>
        <p style="font-size: 1.1rem; color: #666;">Click the Start button to begin your Pomodoro session</p>
    </div>
    """, unsafe_allow_html=True)


st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("### 💡 Pomodoro Tips")

tips_col1, tips_col2 = st.columns(2)

with tips_col1:
    st.markdown("""
    - 🎯 **Stay focused** during study sessions
    - 📵 **Eliminate distractions** before starting
    - ✅ **Complete the full session** without interruption
    """)

with tips_col2:
    st.markdown("""
    - 🚶 **Move around** during breaks
    - 💧 **Stay hydrated** throughout the day
    - 😌 **Relax completely** during break time
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