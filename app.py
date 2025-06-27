# app.py

import streamlit as st
from roadmap_generator import generate_roadmap

st.set_page_config(page_title="PathPlanner.AI", layout="wide")

st.title("🛣️ PathPlanner.AI – Academic Roadmap Generator")
st.markdown("Reverse engineer your dream into a daily learning plan.")

# Input: User's academic/career goal
user_goal = st.text_input("🎯 Enter your goal (e.g., 'Crack GATE 2026', 'Become a Machine Learning Engineer')")

# Input: Duration
weeks = st.slider("📅 Duration (in weeks)", min_value=4, max_value=52, step=1, value=12)

# Submit
if st.button("Generate My Roadmap"):
    if user_goal.strip() == "":
        st.warning("Please enter a valid goal.")
    else:
        with st.spinner("Generating your roadmap..."):
            roadmap = generate_roadmap(user_goal, weeks)
            for week, plan in roadmap.items():
                st.subheader(f"Week {week}")
                st.markdown(f"- **Focus:** {plan['focus']}")
                st.markdown(f"- 📚 Suggested Topics: {', '.join(plan['topics'])}")
                st.markdown("---")
