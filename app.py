import streamlit as st
import json
import os
import random

from roadmap_generator import generate_roadmap
from utils import load_skills, save_progress, load_progress, calculate_progress
from llm_utils import interpret_goal, generate_topic_roadmap, ask_ai
from resource_suggester import fetch_youtube_links
from exporter import save_roadmap_as_pdf

# Setup
st.set_page_config(page_title="PathPlanner.AI", layout="wide")
st.title("📘 PathPlanner.AI – God-Level Academic Roadmap Generator")
st.markdown("🚀 Build your future. Learn anything with AI + smart planning.")

# Load data
skills_db = load_skills("skills_db.json")
with open("resources_db.json", "r") as f:
    static_resources = json.load(f)
progress_data = load_progress("progress.json")

# App mode selection
mode = st.sidebar.radio("Select Mode", [
    "🎯 Goal-to-Curriculum Roadmap",
    "📘 Topic-Focused AI Roadmap",
    "💬 Ask StudyBot"
])

# ------------------ MODE 1: Goal-Based ------------------
if mode == "🎯 Goal-to-Curriculum Roadmap":
    goal = st.text_input("🎯 Enter your learning goal (e.g., Crack GATE 2026):").strip()
    if st.button("🔍 Analyze Goal"):
        if goal:
            ai_output = interpret_goal(goal)
            auto_tracks = ai_output.get("tracks", [])
            auto_topics = ai_output.get("topics", [])

            st.session_state["selected_track"] = auto_tracks[0] if auto_tracks else "general"
            st.session_state["custom_topics"] = auto_topics
            st.success(f"AI selected track: {auto_tracks[0]}")
            st.markdown("### 🧠 Suggested Topics:")
            for t in auto_topics:
                st.markdown(f"- {t}")
        else:
            st.warning("Please enter a valid goal.")

    track = st.session_state.get("selected_track", st.selectbox("📚 Choose a learning track:", list(skills_db.keys())))
    weeks = st.slider("🗓️ Duration (weeks):", 1, 20, 8)

    if st.button("📅 Generate Roadmap"):
        topic_list = st.session_state.get("custom_topics", skills_db[track])
        roadmap = generate_roadmap(topic_list, weeks, goal)
        st.subheader(f"📘 Roadmap for *{goal}* ({weeks} weeks)")

        for week, topics in roadmap.items():
            week_key = f"{goal}_{week}"
            st.markdown(f"### 📆 {week}")
            if week_key not in progress_data:
                progress_data[week_key] = {}
            for topic in topics:
                checked = progress_data[week_key].get(topic, False)
                checked = st.checkbox(f"✅ {topic}", value=checked, key=f"{week}_{topic}")
                progress_data[week_key][topic] = checked

                static_link = static_resources.get(topic)
                if static_link:
                    st.markdown(f"[📘 Static Resource]({static_link})")

        save_progress(progress_data, "progress.json")

        # 🔥 Progress tracking
        progress_percent = calculate_progress(progress_data, goal)
        st.progress(progress_percent / 100)
        st.metric(label="📈 Completion", value=f"{progress_percent}%")

        # 🔽 Export
        if st.button("📤 Download PDF"):
            save_roadmap_as_pdf(roadmap)
            st.success("✅ Saved as study_plan.pdf")

# ------------------ MODE 2: Topic Breakdown ------------------
elif mode == "📘 Topic-Focused AI Roadmap":
    topic = st.text_input("🔍 Enter a topic (e.g., Trigonometry):").strip()
    weeks = st.slider("⏱️ Duration (weeks):", 1, 12, 3)

    if st.button("🧠 Generate AI Roadmap"):
        if topic:
            roadmap = generate_topic_roadmap(topic, weeks)
            if roadmap:
                st.subheader(f"📘 Study Plan for *{topic}*")
                for week, items in roadmap.items():
                    st.markdown(f"### {week}")
                    for item in items:
                        st.markdown(f"- {item}")

                    # 🔗 YouTube search (dynamic)
                    links = fetch_youtube_links(topic)
                    if links:
                        st.markdown("🔗 **Suggested Resources:**")
                        for title, url in links:
                            st.markdown(f"[🎥 {title}]({url})")
            else:
                st.error("❌ Roadmap generation failed.")
        else:
            st.warning("Please enter a topic.")

# ------------------ MODE 3: Ask StudyBot ------------------
elif mode == "💬 Ask StudyBot":
    st.markdown("🤖 Ask anything academic. Example: `What is Bernoulli’s theorem?`")
    query = st.text_area("💬 Your Question:")
    if st.button("📤 Ask"):
        if query:
            response = ask_ai(query)
            st.markdown("### 🤖 StudyBot says:")
            st.markdown(response)
        else:
            st.warning("Ask something first!")
