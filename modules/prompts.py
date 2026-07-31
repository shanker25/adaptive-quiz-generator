# modules/prompts.py - How We Talk to the AI
"""
This module contains all the carefully crafted instructions we give to Gemini AI.
Think of these as detailed recipes that tell the AI exactly how to cook up
the perfect quiz question for you!

Each prompt is like a conversation starter that guides the AI to create
questions at just the right level for you.
"""

class PromptTemplates:
    """
    A collection of smart instruction templates for the AI.
    
    These prompts are like magic spells that make the AI generate
    exactly the kind of questions you need.
    """
    
    @staticmethod
    def get_question_prompt(subject: str, difficulty: str) -> str:
        """
        Create a detailed instruction for generating a quiz question.
        
        This is like giving a chef a recipe - we tell the AI:
        - What subject to focus on
        - How hard the question should be
        - What format the question should take
        
        Args:
            subject: What you're learning about (e.g., "Python", "AI")
            difficulty: How hard the question should be
            
        Returns:
            str: A complete instruction for the AI
        """
        # Each difficulty level gets a different description
        difficulty_descriptions = {
            "Beginner": "basic concepts, definitions, and simple syntax",
            "Easy": "fundamental understanding with simple applications",
            "Medium": "core concepts with moderate complexity",
            "Hard": "advanced concepts and complex scenarios",
            "Expert": "advanced topics, optimizations, and edge cases"
        }
        
        # Pick the right description for this difficulty
        difficulty_desc = difficulty_descriptions.get(difficulty, "core concepts")
        
        # Build the complete instruction
        return f"""Generate one multiple-choice question for {subject} at {difficulty} level.

Focus on testing {difficulty_desc}.

Important guidelines:
1. Question should be educational and test understanding, not memorization
2. Include 4 options labeled A, B, C, D
3. Only one option should be correct
4. Provide a brief but informative explanation (2-3 sentences)

Return ONLY valid JSON with the following structure:
{{
    "question": "Question text here",
    "options": [
        "A. Option 1",
        "B. Option 2",
        "C. Option 3",
        "D. Option 4"
    ],
    "answer": "A. Option 1",
    "explanation": "Brief explanation of why this is the correct answer"
}}

Make sure it's a valid JSON object with exactly these fields."""
    
    @staticmethod
    def get_follow_up_prompt(subject: str, difficulty: str, previous_answer_correct: bool) -> str:
        """
        Create an instruction for the next question based on how you did.
        
        This is smart because it adapts to your performance!
        If you got the last question right, the next one might be a bit harder.
        If you got it wrong, it might be a bit easier.
        
        Args:
            subject: What you're learning about
            difficulty: Current difficulty level
            previous_answer_correct: Did you get the last question right?
            
        Returns:
            str: A tailored instruction for the next question
        """
        # Adjust the instruction based on your performance
        performance = "correctly" if previous_answer_correct else "incorrectly"
        adjustment = "slightly more challenging" if previous_answer_correct else "slightly easier"
        
        return f"""Based on the user's {performance} answer to the previous question, 
        generate a new question about {subject} at {difficulty} level.
        
        Make this question {adjustment} than the previous one while maintaining the {difficulty} level.
        
        Return ONLY valid JSON with the same structure as before:
        {{
            "question": "Question text here",
            "options": ["A. Option 1", "B. Option 2", "C. Option 3", "D. Option 4"],
            "answer": "A. Option 1",
            "explanation": "Brief explanation of the correct answer"
        }}
        """