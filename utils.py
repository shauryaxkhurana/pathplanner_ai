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
