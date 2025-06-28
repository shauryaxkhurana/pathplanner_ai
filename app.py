import streamlit as st
import json
import os
import random

from roadmap_generator import generate_roadmap
from utils import load_skills, save_progress, load_progress, calculate_progress
from llm_utils import interpret_goal, generate_topic_roadmap, ask_ai
from resource_suggester import fetch_youtube_links
from exporter import save_roadmap_as_pdf

# Setup - MUST be first Streamlit command
st.set_page_config(
    page_title="PathPlanner.AI", 
    layout="wide",
    page_icon="🚀",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    /* Main app styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 0;
    }
    
    /* Mode cards */
    .mode-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
        color: #333; /* Fixed text color */
    }

    .mode-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }

    /* Progress styling */
    .progress-container {
        background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        color: white;
    }

    /* Week sections */
    .week-section {
        background: #f8f9ff;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #e1e8ff;
        color: #333; /* Fixed text color */
    }

    /* Resource links */
    .resource-link {
        background: #e3f2fd;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #2196f3;
        color: #333; /* Fixed text color */
    }

    /* Success messages */
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }

    /* Warning messages */
    .warning-message {
        background: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #ffeaa7;
        margin: 1rem 0;
    }

    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e1e8ff;
        transition: border-color 0.3s ease;
    }

    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }

    /* Button styling */
    .stButton > button {
        border-radius: 8px;
        border: none;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }

    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# Enhanced header
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🚀 PathPlanner.AI</h1>
    <p class="main-subtitle">Your AI-Powered Learning Companion - Master Any Subject with Smart Planning</p>
</div>
""", unsafe_allow_html=True)

# Load data
try:
    skills_db = load_skills("skills_db.json")
    with open("resources_db.json", "r") as f:
        static_resources = json.load(f)
    progress_data = load_progress("progress.json")
except FileNotFoundError as e:
    st.error(f"❌ Error loading data files: {e}")
    st.stop()

# Enhanced sidebar
with st.sidebar:
    st.markdown("### 🎯 Choose Your Learning Path")
    mode = st.radio(
        "",
        [
            "🎯 Goal-to-Curriculum Roadmap",
            "📘 Topic-Focused AI Roadmap",
            "💬 Ask StudyBot"
        ],
        help="Select the learning mode that best fits your needs"
    )
    
    st.markdown("---")
    st.markdown("### 📊 Quick Stats")
    total_progress = sum(calculate_progress(progress_data, goal) for goal in progress_data.keys()) / max(len(progress_data), 1)
    st.metric("Overall Progress", f"{total_progress:.1f}%")
    st.metric("Active Goals", len(progress_data))

# Create three columns for better layout
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # ------------------ MODE 1: Goal-Based ------------------
    if mode == "🎯 Goal-to-Curriculum Roadmap":
        st.markdown("""
        <div class="mode-card">
            <h3>🎯 Goal-Based Learning</h3>
            <p>Transform your ambitious goals into structured learning plans. Our AI analyzes your objective and creates a personalized roadmap.</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.container():
            st.markdown("### Step 1: Define Your Goal")
            goal = st.text_input(
                "🎯 What do you want to achieve?", 
                placeholder="e.g., Crack GATE 2026, Master Machine Learning, Learn Web Development",
                help="Be specific about your learning objective"
            ).strip()
            
            col_analyze, col_space = st.columns([1, 3])
            with col_analyze:
                analyze_clicked = st.button("🔍 Analyze Goal", type="primary")
            
            if analyze_clicked:
                if goal:
                    with st.spinner("🧠 AI is analyzing your goal..."):
                        try:
                            ai_output = interpret_goal(goal)
                            auto_tracks = ai_output.get("tracks", [])
                            auto_topics = ai_output.get("topics", [])

                            st.session_state["selected_track"] = auto_tracks[0] if auto_tracks else "general"
                            st.session_state["custom_topics"] = auto_topics
                            
                            st.markdown(f"""
                            <div class="success-message">
                                ✅ <strong>Goal Analysis Complete!</strong><br>
                                AI selected track: <strong>{auto_tracks[0] if auto_tracks else 'General'}</strong>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if auto_topics:
                                st.markdown("### 🧠 AI-Suggested Topics:")
                                topic_cols = st.columns(2)
                                for i, topic in enumerate(auto_topics):
                                    with topic_cols[i % 2]:
                                        st.markdown(f"• **{topic}**")
                        except Exception as e:
                            st.error(f"❌ Error analyzing goal: {e}")
                else:
                    st.markdown("""
                    <div class="warning-message">
                        ⚠️ Please enter a valid learning goal to continue.
                    </div>
                    """, unsafe_allow_html=True)

        if goal:
            st.markdown("### Step 2: Customize Your Plan")
            col_track, col_weeks = st.columns(2)
            
            with col_track:
                track = st.session_state.get(
                    "selected_track", 
                    st.selectbox("📚 Learning Track:", list(skills_db.keys()))
                )
            
            with col_weeks:
                weeks = st.slider("🗓️ Duration (weeks):", 1, 20, 8, help="Choose your preferred timeline")

            st.markdown("### Step 3: Generate Your Roadmap")
            if st.button("📅 Generate Roadmap", type="primary"):
                with st.spinner("🚀 Creating your personalized roadmap..."):
                    try:
                        topic_list = st.session_state.get("custom_topics", skills_db[track])
                        roadmap = generate_roadmap(topic_list, weeks, goal)
                        
                        st.markdown(f"""
                        <div class="progress-container">
                            <h2>📘 Your Learning Roadmap: {goal}</h2>
                            <p>Duration: {weeks} weeks | Track: {track}</p>
                        </div>
                        """, unsafe_allow_html=True)

                        for week, topics in roadmap.items():
                            week_key = f"{goal}_{week}"
                            
                            st.markdown(f"""
                            <div class="week-section">
                                <h3>📆 {week}</h3>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if week_key not in progress_data:
                                progress_data[week_key] = {}
                                
                            topic_cols = st.columns(2)
                            for i, topic in enumerate(topics):
                                with topic_cols[i % 2]:
                                    checked = progress_data[week_key].get(topic, False)
                                    checked = st.checkbox(
                                        f"✅ {topic}", 
                                        value=checked, 
                                        key=f"{week}_{topic}"
                                    )
                                    progress_data[week_key][topic] = checked

                                    static_link = static_resources.get(topic)
                                    if static_link:
                                        st.markdown(f"""
                                        <div class="resource-link">
                                            <a href="{static_link}" target="_blank">📘 Study Resource</a>
                                        </div>
                                        """, unsafe_allow_html=True)

                        save_progress(progress_data, "progress.json")

                        # Enhanced progress tracking
                        progress_percent = calculate_progress(progress_data, goal)
                        st.markdown("### 📈 Your Progress")
                        progress_col1, progress_col2 = st.columns(2)
                        
                        with progress_col1:
                            st.progress(progress_percent / 100)
                        with progress_col2:
                            st.metric("Completion", f"{progress_percent}%", delta=f"{progress_percent}%")

                        # Export option
                        if st.button("📤 Download PDF", help="Export your roadmap as a PDF"):
                            save_roadmap_as_pdf(roadmap)
                            st.success("✅ Roadmap saved as study_plan.pdf")
                    
                    except Exception as e:
                        st.error(f"❌ Error generating roadmap: {e}")

    # ------------------ MODE 2: Topic Breakdown ------------------
    elif mode == "📘 Topic-Focused AI Roadmap":
        st.markdown("""
        <div class="mode-card">
            <h3>📘 Deep Topic Exploration</h3>
            <p>Dive deep into any specific topic with AI-generated study plans and curated resources.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Explore Any Topic In-Depth")
        
        col_topic, col_weeks = st.columns([2, 1])
        with col_topic:
            topic = st.text_input(
                "🔍 Topic to Master", 
                placeholder="e.g., Trigonometry, Machine Learning, Organic Chemistry",
                help="Enter any academic topic you want to learn"
            ).strip()
        
        with col_weeks:
            weeks = st.slider("⏱️ Study Duration:", 1, 12, 3)

        if st.button("🧠 Generate AI Study Plan", type="primary"):
            if topic:
                with st.spinner(f"🚀 Creating detailed study plan for {topic}..."):
                    try:
                        roadmap = generate_topic_roadmap(topic, weeks)
                        if roadmap:
                            st.markdown(f"""
                            <div class="progress-container">
                                <h2>📘 Master {topic} in {weeks} Weeks</h2>
                                <p>AI-Generated Comprehensive Study Plan</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            for week, items in roadmap.items():
                                st.markdown(f"""
                                <div class="week-section">
                                    <h3>{week}</h3>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                item_cols = st.columns(1)
                                for item in items:
                                    st.markdown(f"• **{item}**")

                                # YouTube resources
                                with st.spinner("🔗 Finding relevant video resources..."):
                                    links = fetch_youtube_links(f"{topic} {week}")
                                    if links:
                                        st.markdown("#### 🎥 Recommended Videos:")
                                        video_cols = st.columns(2)
                                        for i, (title, url) in enumerate(links[:4]):  # Limit to 4 videos
                                            with video_cols[i % 2]:
                                                st.markdown(f"[🎥 {title[:50]}...]({url})")
                        else:
                            st.error("❌ Unable to generate roadmap. Please try a different topic.")
                    except Exception as e:
                        st.error(f"❌ Error generating study plan: {e}")
            else:
                st.markdown("""
                <div class="warning-message">
                    ⚠️ Please enter a topic to generate your study plan.
                </div>
                """, unsafe_allow_html=True)

    # ------------------ MODE 3: Ask StudyBot ------------------
    elif mode == "💬 Ask StudyBot":
        st.markdown("""
        <div class="mode-card">
            <h3>🤖 AI Study Assistant</h3>
            <p>Get instant answers to your academic questions. Ask about concepts, problems, or study strategies.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Chat with Your AI Tutor")
        
        # Example questions
        with st.expander("💡 Example Questions"):
            st.markdown("""
            • What is Bernoulli's theorem and how is it applied?
            • Explain the difference between supervised and unsupervised learning
            • How do I solve quadratic equations step by step?
            • What are the best study techniques for memorizing formulas?
            • Can you explain photosynthesis in simple terms?
            """)
        
        query = st.text_area(
            "💬 Ask me anything academic:", 
            height=100,
            placeholder="Type your question here... I can explain concepts, solve problems, or give study advice!"
        )
        
        if st.button("📤 Get Answer", type="primary"):
            if query:
                with st.spinner("🤖 StudyBot is thinking..."):
                    try:
                        response = ask_ai(query)
                        
                        st.markdown("""
                        <div class="mode-card">
                            <h4>🤖 StudyBot's Response:</h4>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(response)
                        
                        # Follow-up suggestions
                        st.markdown("### 💡 Follow-up Questions:")
                        follow_up_cols = st.columns(2)
                        with follow_up_cols[0]:
                            if st.button("🔍 Can you explain this further?"):
                                st.text_area("Follow-up:", value=f"Can you explain '{query}' in more detail?")
                        with follow_up_cols[1]:
                            if st.button("📝 Give me practice problems"):
                                st.text_area("Follow-up:", value=f"Can you give me practice problems for '{query}'?")
                    
                    except Exception as e:
                        st.error(f"❌ Error getting response: {e}")
            else:
                st.markdown("""
                <div class="warning-message">
                    ⚠️ Please ask a question to get started with StudyBot!
                </div>
                """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>🚀 <strong>PathPlanner.AI</strong> - Empowering learners worldwide with AI-driven education</p>
    <p>Made with ❤️ for ambitious learners</p>
</div>
""", unsafe_allow_html=True)