import streamlit as st
import json
import os
import random
from roadmap_generator import generate_roadmap
from utils import load_skills, save_progress, load_progress

# Page setup
st.set_page_config(page_title="PathPlanner.AI", layout="wide")

st.title("📘 PathPlanner.AI – Academic Roadmap Generator")
st.markdown("🚀 Plan your study journey, track your progress, and stay motivated!")

# Load skills and resources
skills_db = load_skills("skills_db.json")
with open("resources_db.json", "r") as f:
    resources = json.load(f)

# Load or initialize progress data
progress_data = load_progress("progress.json")

# Goal input
goal = st.text_input("🎯 Enter your learning goal (e.g., Crack GATE 2026):").strip()

# Skill area selection
track = st.selectbox("📚 Choose a learning track:", list(skills_db.keys()))

# Duration
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

# Generate button
if st.button("📅 Generate Roadmap"):
    if goal and track:
        st.subheader(f"🧠 Roadmap for: *{goal}* ({track}, {weeks} weeks)")
        roadmap = generate_roadmap(skills_db[track], weeks)
        for week, topics in roadmap.items():
            week_key = f"{goal}_{week}"
            st.markdown(f"### 📆 {week}")
            if week_key not in progress_data:
                progress_data[week_key] = {}
            for topic in topics:
                checked = progress_data[week_key].get(topic, False)
                checked = st.checkbox(f"✅ {topic}", value=checked, key=f"{week}_{topic}")
                progress_data[week_key][topic] = checked

                # Show resource link
                resource_link = resources.get(topic)
                if resource_link:
                    st.markdown(f"[📘 Learn More]({resource_link})")

        # Save progress
        save_progress(progress_data, "progress.json")

        # Show motivational quote
        st.success(random.choice(affirmations))
    else:
        st.warning("Please enter a goal and select a learning track.")
