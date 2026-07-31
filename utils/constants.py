# utils/constants.py - All Your Quiz Settings in One Place
"""
This is the control center for your quiz app!

Everything you can customize is right here:
- What subjects are available
- What difficulty levels exist
- How many questions per quiz
- Messages and colors

Think of this as the dashboard where you can tune
your quiz experience!
"""

# ============================================================
# DIFFICULTY LEVELS - The Learning Ladder
# ============================================================
# Each level represents a step in your learning journey
DIFFICULTY_LEVELS = ["Beginner", "Easy", "Medium", "Hard", "Expert"]

# ============================================================
# AVAILABLE SUBJECTS - What You Can Learn
# ============================================================
# Add or remove subjects here to customize your quiz
SUBJECTS = [
    # Programming Languages - The building blocks of software
    "Python",
    "Java",
    "JavaScript",
    "C++",
    "Ruby",
    "Go",
    "Rust",
    
    # Artificial Intelligence - The future of technology
    "AI",
    "Machine Learning",
    "Deep Learning",
    "Natural Language Processing",
    
    # Development - Building amazing applications
    "Web Development",
    "Data Science",
    "Cloud Computing",
    "DevOps",
    
    # Security - Keeping data safe
    "Cybersecurity",
    
    # Emerging Tech - The next big things
    "Blockchain",
    
    # Data - The new oil
    "Database Management"
]

# ============================================================
# DEFAULT SETTINGS - How Your Quiz Behaves
# ============================================================
# These are the starting values for your quiz
DEFAULT_SETTINGS = {
    'total_questions': 10,        # Default number of questions
    'min_questions': 5,           # Minimum allowed
    'max_questions': 15,          # Maximum allowed
    'initial_difficulty': 'Medium' # Where to start
}

# ============================================================
# PERFORMANCE THRESHOLDS - How We Evaluate Your Results
# ============================================================
# These percentages determine your achievement level
PERFORMANCE = {
    'excellent': 80,    # 80% and above = Expert!
    'good': 60,         # 60-79% = Good job!
    'needs_improvement': 0  # Below 60% = Keep practicing!
}

# ============================================================
# UI MESSAGES - Encouraging Words for You
# ============================================================
# These are the messages you'll see based on your performance
MESSAGES = {
    'excellent': "🌟 Excellent! You're a subject expert!",
    'good': "👍 Good job! Keep learning and improving.",
    'needs_improvement': "📚 Keep practicing! You'll get better."
}

# ============================================================
# DIFFICULTY COLORS - Visual Feedback
# ============================================================
# Each difficulty level gets its own color for easy recognition
DIFFICULTY_COLORS = {
    "Beginner": "#4CAF50",  # Green - easy going
    "Easy": "#8BC34A",      # Light Green - getting there
    "Medium": "#FFC107",    # Yellow - middle ground
    "Hard": "#FF9800",      # Orange - challenging
    "Expert": "#F44336"     # Red - expert level!
}