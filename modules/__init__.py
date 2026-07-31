# modules/__init__.py
"""
Welcome to the Brain of Your Quiz App!

This package contains all the smart components that make your quiz work:
- llm.py: Talks to Gemini AI to generate questions
- prompts.py: Holds the instructions we give to the AI
- adaptive.py: Decides if your next question should be easier or harder
- parser.py: Reads and understands the AI's responses
- quiz_manager.py: Orchestrates the entire quiz experience

Together, these modules work like a well-oiled machine to create
a personalized learning experience just for you!
"""

# Make these modules easily accessible
from .llm import GeminiClient
from .prompts import PromptTemplates
from .adaptive import DifficultyManager
from .parser import ResponseParser
from .quiz_manager import QuizManager

# Tell Python what to import when someone uses "from modules import *"
__all__ = [
    'GeminiClient',
    'PromptTemplates',
    'DifficultyManager',
    'ResponseParser',
    'QuizManager'
]