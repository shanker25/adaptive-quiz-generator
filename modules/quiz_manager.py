# modules/quiz_manager.py - The Quiz Flow Controller
import streamlit as st
from datetime import datetime

class QuizManager:
    def __init__(self, llm_client, parser, difficulty_manager, prompt_templates):
        self.llm_client = llm_client
        self.parser = parser
        self.difficulty_manager = difficulty_manager
        self.prompt_templates = prompt_templates

    def start_quiz(self, subject: str, total_questions: int, starting_difficulty: str):
        st.session_state.quiz_started = True
        st.session_state.quiz_complete = False
        st.session_state.subject = subject
        st.session_state.total_questions = total_questions
        st.session_state.questions_asked = 0
        st.session_state.correct_answers = 0
        st.session_state.current_difficulty = starting_difficulty
        st.session_state.score_history = []
        st.session_state.difficulty_history = []
        st.session_state.start_time = datetime.now()
        st.session_state.answer_submitted = False
        st.session_state.selected_answer = None
        # Reset fallback trackers
        st.session_state.parser_used_fallbacks = []
        st.session_state.qm_used_fallbacks = []
        self._generate_new_question()

    def next_question(self, is_correct: bool):
        st.session_state.current_difficulty = self.difficulty_manager.adjust_difficulty(
            st.session_state.current_difficulty,
            is_correct
        )
        self._generate_new_question()
        st.session_state.answer_submitted = False
        st.session_state.selected_answer = None

    def _generate_new_question(self):
        try:
            prompt = self.prompt_templates.get_question_prompt(
                subject=st.session_state.subject,
                difficulty=st.session_state.current_difficulty
            )
            prompt += "\n\nMake this question unique and different from all others. Use a creative scenario."
            response_text = self.llm_client.generate_content(prompt)
            question_data = self.parser.parse_response(response_text)
            st.session_state.current_question = question_data
        except Exception as e:
            st.error(f"⚠️ AI error, using fallback: {str(e)}")
            st.session_state.current_question = self._get_fallback_question()

    def _get_fallback_question(self) -> dict:
        subject = st.session_state.subject
        pool = [
            {
                "question": f"What is a key principle in {subject}?",
                "options": [
                    "A. Understanding fundamentals",
                    "B. Memorizing everything",
                    "C. Avoiding practice",
                    "D. Copying others"
                ],
                "answer": "A. Understanding fundamentals",
                "explanation": "Strong fundamentals are the foundation of expertise."
            },
            {
                "question": f"How do you excel at {subject}?",
                "options": [
                    "A. Hands-on practice",
                    "B. Reading theory only",
                    "C. Watching videos",
                    "D. Doing nothing"
                ],
                "answer": "A. Hands-on practice",
                "explanation": "Applying knowledge solidifies learning."
            },
            {
                "question": f"What is the most common mistake in {subject}?",
                "options": [
                    "A. Skipping basics",
                    "B. Asking questions",
                    "C. Reviewing mistakes",
                    "D. Seeking feedback"
                ],
                "answer": "A. Skipping basics",
                "explanation": "Without a solid foundation, advanced concepts are hard."
            },
            {
                "question": f"Why is {subject} important?",
                "options": [
                    "A. It solves real-world problems",
                    "B. It's just theory",
                    "C. It's outdated",
                    "D. It's optional"
                ],
                "answer": "A. It solves real-world problems",
                "explanation": "Practical applications drive value in any field."
            },
            {
                "question": f"What is the first step to master {subject}?",
                "options": [
                    "A. Build a strong foundation",
                    "B. Memorize everything",
                    "C. Jump to advanced topics",
                    "D. Ignore fundamentals"
                ],
                "answer": "A. Build a strong foundation",
                "explanation": "Lay the groundwork before moving ahead."
            },
            {
                "question": f"What helps you stay motivated in {subject}?",
                "options": [
                    "A. Small wins",
                    "B. Long breaks",
                    "C. Avoiding challenges",
                    "D. Comparing with others"
                ],
                "answer": "A. Small wins",
                "explanation": "Progress, however small, keeps you going."
            },
            {
                "question": f"What is a common myth about {subject}?",
                "options": [
                    "A. You need talent",
                    "B. You need tools",
                    "C. You need time",
                    "D. You need help"
                ],
                "answer": "A. You need talent",
                "explanation": "Effort and strategy trump innate talent."
            },
            {
                "question": f"How does collaboration help in {subject}?",
                "options": [
                    "A. Diverse perspectives",
                    "B. Distraction",
                    "C. Dependency",
                    "D. Competitiveness"
                ],
                "answer": "A. Diverse perspectives",
                "explanation": "Working with others expands your understanding."
            },
            {
                "question": f"What is the best resource for {subject}?",
                "options": [
                    "A. Official documentation",
                    "B. Random blogs",
                    "C. YouTube videos",
                    "D. Social media"
                ],
                "answer": "A. Official documentation",
                "explanation": "Primary sources provide accurate and reliable information."
            },
            {
                "question": f"How do you stay current in {subject}?",
                "options": [
                    "A. Following industry news",
                    "B. Ignoring updates",
                    "C. Sticking to old materials",
                    "D. Avoiding changes"
                ],
                "answer": "A. Following industry news",
                "explanation": "Staying updated ensures you're learning relevant knowledge."
            }
        ]

        if 'qm_used_fallbacks' not in st.session_state:
            st.session_state.qm_used_fallbacks = []
        used = st.session_state.qm_used_fallbacks

        if len(used) == len(pool):
            used.clear()

        available = [i for i in range(len(pool)) if i not in used]
        idx = available[0]
        used.append(idx)
        return pool[idx]