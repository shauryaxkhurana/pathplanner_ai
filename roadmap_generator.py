import json
import random

def load_skills():
    with open("skills_db.json", "r") as file:
        skills_map = json.load(file)
    return skills_map

def generate_roadmap(user_goal, total_weeks):
    skills_map = load_skills()

    # Simple matching: find skill domain related to goal
    matched_skills = []
    for category, skills in skills_map.items():
        if category.lower() in user_goal.lower():
            matched_skills.extend(skills)

    # Fallback: use default/general skills
    if not matched_skills:
        matched_skills = skills_map.get("general", [])

    # Divide skills into weekly chunks
    random.shuffle(matched_skills)
    weekly_plan = {}
    skills_per_week = max(1, len(matched_skills) // total_weeks)

    for week in range(1, total_weeks + 1):
        start = (week - 1) * skills_per_week
        end = start + skills_per_week
        topics = matched_skills[start:end]
        if not topics:
            topics = ["Revision / Practice"]

        weekly_plan[week] = {
            "focus": f"Learning {topics[0]}" if topics[0] != "Revision / Practice" else topics[0],
            "topics": topics
        }

    return weekly_plan
