# modules/adaptive.py - The Smart Difficulty Adjuster
"""
This is the brain that decides if your next question should be harder or easier.
It's like having a personal coach who knows exactly when to challenge you
and when to give you a break!

The difficulty levels work like a ladder:
Beginner → Easy → Medium → Hard → Expert

If you get questions right, you climb up the ladder.
If you get them wrong, you go down a step.
"""

from utils.constants import DIFFICULTY_LEVELS

class DifficultyManager:
    """
    Your personal difficulty coach!
    
    This smart manager:
    1. Knows all the difficulty levels
    2. Tracks your performance
    3. Adjusts the challenge level just for you
    """
    
    def __init__(self):
        """Get ready to manage difficulty levels"""
        self.difficulty_levels = DIFFICULTY_LEVELS
    
    def get_difficulty_index(self, difficulty: str) -> int:
        """
        Find where a difficulty level is in the ladder.
        
        Example: "Beginner" is at position 0, "Expert" is at position 4.
        
        Args:
            difficulty: The difficulty level name
            
        Returns:
            int: Position in the difficulty ladder
        """
        try:
            return self.difficulty_levels.index(difficulty)
        except ValueError:
            # If the level isn't found, start at Medium
            return self.difficulty_levels.index("Medium")
    
    def adjust_difficulty(self, current_difficulty: str, is_correct: bool) -> str:
        """
        The smart decision-maker!
        
        This is where the magic happens:
        - Got it right? Let's try something a bit harder!
        - Got it wrong? Let's take a step back and make it easier.
        
        Args:
            current_difficulty: Where you are now
            is_correct: Did you answer correctly?
            
        Returns:
            str: Your new difficulty level
        """
        # Find where you are on the difficulty ladder
        current_index = self.get_difficulty_index(current_difficulty)
        
        if is_correct:
            # You're doing great! Let's move up one level
            if current_index < len(self.difficulty_levels) - 1:
                return self.difficulty_levels[current_index + 1]
        else:
            # Oops! Let's make it a bit easier
            if current_index > 0:
                return self.difficulty_levels[current_index - 1]
        
        # If you can't go up or down, stay where you are
        return current_difficulty
    
    def get_difficulty_description(self, difficulty: str) -> str:
        """
        Get a friendly description of what each difficulty means.
        
        This helps you understand what to expect at each level.
        
        Args:
            difficulty: The difficulty level
            
        Returns:
            str: A description with emojis!
        """
        descriptions = {
            "Beginner": "📘 Fundamental concepts and basic definitions",
            "Easy": "📗 Simple problems with straightforward solutions",
            "Medium": "📙 Moderate complexity requiring understanding of core concepts",
            "Hard": "📕 Challenging problems requiring deep understanding",
            "Expert": "📘 Advanced topics requiring mastery of the subject"
        }
        return descriptions.get(difficulty, "Unknown difficulty level")
    
    def get_average_difficulty(self, difficulty_history: list) -> str:
        """
        Calculate your average difficulty level across the quiz.
        
        This gives you a sense of how challenging the quiz was overall.
        
        Args:
            difficulty_history: List of all difficulty levels you've seen
            
        Returns:
            str: The average difficulty level
        """
        if not difficulty_history:
            return "N/A"
        
        # Convert difficulty names to numbers
        indices = [self.get_difficulty_index(d) for d in difficulty_history]
        
        # Calculate the average position
        avg_index = sum(indices) / len(indices)
        rounded_index = round(avg_index)
        
        # Make sure the index is valid
        rounded_index = max(0, min(rounded_index, len(self.difficulty_levels) - 1))
        
        return self.difficulty_levels[rounded_index]
    
    def get_difficulty_color(self, difficulty: str) -> str:
        """
        Get a color that represents each difficulty level.
        
        Green for easy, yellow for medium, red for hard!
        
        Args:
            difficulty: The difficulty level
            
        Returns:
            str: A color code for styling
        """
        colors = {
            "Beginner": "#4CAF50",  # Green
            "Easy": "#8BC34A",      # Light Green
            "Medium": "#FFC107",    # Yellow
            "Hard": "#FF9800",      # Orange
            "Expert": "#F44336"     # Red
        }
        return colors.get(difficulty, "#888888")  # Gray if not found