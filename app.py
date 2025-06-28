import streamlit as st
import json
import os
import random
from roadmap_generator import generate_roadmap
from utils import load_skills, save_progress, load_progress
from llm_utils import interpret_goal

# Page setup
st.set_page_config(page_title="PathPlanner.AI", layout="wide")
st.title("📘 PathPlanner.AI – AI-Powered Academic Roadmap Generator")
st.markdown("🚀 Plan your study journey with AI, track progress, and stay motivated!")

# Load skills and resources
skills_db = load_skills("skills_db.json")
with open("resources_db.json", "r") as f:
    resources = json.load(f)

# Load or initialize progress data
progress_data = load_progress("progress.json")

# Goal input
goal = st.text_input("🎯 Enter your learning goal (e.g., Crack GATE 2026):").strip()

# AI Track and Topic Interpretation
if st.button("🔍 Understand My Goal with AI"):
    if goal:
        ai_output = interpret_goal(goal)
        auto_tracks = ai_output.get("tracks", [])
        auto_topics = ai_output.get("topics", [])

        st.session_state["selected_track"] = auto_tracks[0] if auto_tracks else "general"
        st.session_state["custom_topics"] = auto_topics

        st.success(f"AI selected track: {auto_tracks[0]}")
        st.markdown("### 🧠 Suggested Topics by AI:")
        for t in auto_topics:
            st.markdown(f"- {t}")
    else:
        st.warning("Please enter a goal to interpret.")

# Final track selection
track = st.session_state.get("selected_track", st.selectbox("📚 Choose a learning track:", list(skills_db.keys())))
weeks = st.slider("🗓️ Select duration (in weeks):", 1, 20, 8)

# Affirmations
affirmations = [
    "You're doing great — one step at a time.",
    "Progress over perfection!",
    "Stay consistent, you're closer than you think.",
    "Believe in yourself, always.",
    "Even slow progress is progress.",
    "Your future self will thank you.",
    "Stay focused. You got this!"
]

# Generate roadmap
if st.button("📅 Generate Roadmap"):
    topic_list = st.session_state.get("custom_topics", skills_db[track])
    roadmap = generate_roadmap(topic_list, weeks, goal)
    st.subheader(f"🧠 Roadmap for: *{goal}* ({track}, {weeks} weeks)")

    for week, topics in roadmap.items():
        week_key = f"{goal}_{week}"
        st.markdown(f"### 📆 {week}")
        if week_key not in progress_data:
            progress_data[week_key] = {}
        for topic in topics:
            checked = progress_data[week_key].get(topic, False)
            checked = st.checkbox(f"✅ {topic}", value=checked, key=f"{week}_{topic}")
            progress_data[week_key][topic] = checked

            resource_link = resources.get(topic)
            if resource_link:
                st.markdown(f"[📘 Learn More]({resource_link})")

    save_progress(progress_data, "progress.json")
    st.success(random.choice(affirmations))
