def generate_roadmap(topics, weeks, user_goal=None):
    roadmap = {}

    if user_goal:
        goal_lower = user_goal.lower()
        if "gate" in goal_lower:
            topics = sorted(topics)
        elif "class 10" in goal_lower or "cbse" in goal_lower:
            topics = topics
        elif "ml" in goal_lower or "machine learning" in goal_lower:
            topics = topics[::-1]

    total_topics = len(topics)
    topics_per_week = total_topics // weeks
    remainder = total_topics % weeks

    idx = 0
    for week in range(1, weeks + 1):
        count = topics_per_week + (1 if week <= remainder else 0)
        roadmap[f"Week {week}"] = topics[idx: idx + count]
        idx += count

    return roadmap
