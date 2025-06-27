def get_affirmation(progress_percent):
    if progress_percent == 0:
        return "🚀 Just getting started? Let’s crush Week 1!"
    elif progress_percent < 40:
        return "🔥 Keep pushing! Small steps make big changes."
    elif progress_percent < 70:
        return "💪 You're doing well — stay consistent!"
    elif progress_percent < 90:
        return "🌟 Almost there! Let’s finish strong!"
    elif progress_percent < 100:
        return "🏁 Final push — don’t leave any topic behind!"
    else:
        return "🎉 Incredible! You’ve nailed this week!"
