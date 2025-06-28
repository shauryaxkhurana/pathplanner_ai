import ollama
import json
import re

def interpret_goal(user_goal):
    prompt = f'''
    You are an expert academic advisor. Given this user's goal: "{user_goal}",
    identify:
    1. Suitable learning tracks (choose from: class 10, class 11, class 12, GATE, machine learning, general)
    2. 10 most important topics or skills they should study

    Respond in this JSON format:
    {{
        "tracks": [...],
        "topics": [...]
    }}
    '''
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    match = re.search(r'\{.*\}', response['message']['content'], re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return {"tracks": [], "topics": []}
    return {"tracks": [], "topics": []}
