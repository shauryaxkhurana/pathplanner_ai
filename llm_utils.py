import json
import re
import ollama

# 🧠 Interpret a full learning goal and extract track + topics
def interpret_goal(user_goal):
    prompt = f"""
    You are a smart academic advisor.
    Interpret this learning goal: "{user_goal}"
    1. Suggest the most relevant academic track (e.g., 'gate', 'class 10', 'machine learning')
    2. Suggest 8-10 key topics the user should cover.

    Respond in this format:
    {{
      "tracks": ["..."],
      "topics": ["...", "..."]
    }}
    """
    response = ollama.chat(
        model="mistral:instruct",
        messages=[{"role": "user", "content": prompt}]
    )
    try:
        json_block = re.search(r'\{.*\}', response['message']['content'], re.DOTALL)
        return json.loads(json_block.group(0)) if json_block else {}
    except:
        return {}

# 📘 Break a specific topic into a week-wise roadmap
def generate_topic_roadmap(topic, weeks):
    prompt = f"""
    Break down the topic "{topic}" into a detailed roadmap for {weeks} weeks.
    Each week should contain 2-3 logically connected subtopics or skills.

    Respond in JSON format like:
    {{
        "Week 1": ["...", "..."],
        "Week 2": ["...", "..."]
    }}
    """
    response = ollama.chat(
        model="mistral:instruct",
        messages=[{"role": "user", "content": prompt}]
    )
    try:
        json_block = re.search(r'\{.*\}', response['message']['content'], re.DOTALL)
        return json.loads(json_block.group(0)) if json_block else {}
    except:
        return {}

# 💬 Ask anything (StudyBot)
def ask_ai(query):
    response = ollama.chat(
        model="mistral:instruct",
        messages=[
            {"role": "system", "content": "You are a helpful, friendly academic tutor who explains things clearly."},
            {"role": "user", "content": query}
        ]
    )
    return response["message"]["content"]
