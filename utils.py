import json
import os

def load_skills(path):
    with open(path, "r") as f:
        return json.load(f)

def load_progress(path):
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump({}, f)
    with open(path, "r") as f:
        return json.load(f)

def save_progress(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def calculate_progress(progress_data, goal_prefix=""):
    completed = 0
    total = 0
    for week_key, week_topics in progress_data.items():
        if goal_prefix and not week_key.startswith(goal_prefix):
            continue
        for topic, done in week_topics.items():
            total += 1
            if done:
                completed += 1
    if total == 0:
        return 0
    return round((completed / total) * 100, 2)
