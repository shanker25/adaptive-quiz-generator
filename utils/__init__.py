# utils/__init__.py
"""
Welcome to the Utility Toolkit!

This package contains helpful tools that make your app work better:
- constants.py: All the settings and options
- helpers.py: Reusable functions for the user interface

These utilities are like the Swiss Army knife of your app -
they contain handy tools that are used throughout the application!
"""

# Make everything easily accessible
from .constants import *
from .helpers import *

# Tell Python what to import when someone uses "from utils import *"
__all__ = [
    'DIFFICULTY_LEVELS',
    'SUBJECTS',
    'DEFAULT_SETTINGS',
    'display_metrics',
    'show_question',
    'show_explanation',
    'get_performance_message',
    'render_results_page'
]