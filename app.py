import streamlit as st
import os
import json
from roadmap_generator import generate_roadmap

# --- App Configuration ---
st.set_page_config(page_title="PathPlanner.AI", layout="wide")
st.title("🛣️ PathPlanner.AI – Academic Roadmap Generator")
st.markdown("Reverse engineer your academic goals into personalized weekly study plans.")

# --- Load External Files ---
def load_progress():
    if os.path.exists("progress.json"):
        with open("progress.json", "r") as f:
            return json.load(f)
    return {}

def save_progress(progress):
    with open("progress.json", "w") as f:
        json.dump(progress, f, indent=2)

# Load progress and resources
progress_data = load_progress()
with open("resources_db.json", "r") as f:
    resources = json.load(f)

# --- User Input ---
user_goal = st.text_input("🎯 Enter your goal", placeholder="e.g. Crack GATE 2026, Master Class 10th Math")
weeks = st.slider("📅 Select Duration (weeks)", min_value=4, max_value=52, value=12)

# --- Generate Roadmap ---
if st.button("Generate My Roadmap"):
    if user_goal.strip() == "":
        st.warning("Please enter a valid goal.")
    else:
        with st.spinner("Generating your roadmap..."):
            roadmap = generate_roadmap(user_goal, weeks)
            st.success("Here is your personalized weekly plan:")

            for week, plan in roadmap.items():
                st.subheader(f"📅 Week {week} – Focus: {plan['focus']}")

                week_key = f"{user_goal}_week_{week}"
                if week_key not in progress_data:
                    progress_data[week_key] = {topic: False for topic in plan['topics']}

                for topic in plan['topics']:
                    checkbox_key = f"{week_key}_{topic}"
                    checked = st.checkbox(f"{topic}", value=progress_data[week_key].get(topic, False), key=checkbox_key)
                    progress_data[week_key][topic] = checked

                    # Show learning resource if available
                    resource_link = resources.get(topic)
                    if resource_link:
                        st.markdown(f"[📘 Learn More]({resource_link})")

                st.markdown("---")

            # Save progress
            save_progress(progress_data)
