# app.py - Your Interactive Quiz Application
# This is where everything comes together to create a fun learning experience

import streamlit as st
from modules.quiz_manager import QuizManager
from modules.adaptive import DifficultyManager
from modules.llm import GeminiClient
from modules.parser import ResponseParser
from modules.prompts import PromptTemplates
from utils.constants import SUBJECTS, DIFFICULTY_LEVELS, DEFAULT_SETTINGS
from utils.helpers import (
    display_metrics, 
    show_question, 
    show_explanation,
    render_results_page
)
import os
from dotenv import load_dotenv

# Load your secret API keys from a safe place
load_dotenv()

# ============================================================
# STEP 1: Set up the look and feel of your app
# ============================================================

# Give your app a name and icon that appears in the browser tab
st.set_page_config(
    page_title="🧠 Adaptive AI Quiz Generator",
    page_icon="🧠",
    layout="wide"
)

# Add some custom style to make things look pretty
st.markdown("""
<style>
    /* A beautiful gradient header for your app */
    .main-header {
        text-align: center;
        padding: 1.5rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    /* Make all buttons full width and rounded */
    .stButton button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
    }
    /* A clean box for showing explanations */
    .explanation-box {
        padding: 1rem;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# STEP 2: The Main Quiz App - Your Learning Companion
# ============================================================

class QuizApp:
    """
    This is your main quiz application.
    Think of it as the friendly host that guides you through the learning journey.
    """
    
    def __init__(self):
        """
        Welcome to the quiz! Here's what happens when you start:
        1. We connect to Gemini AI (our clever question generator)
        2. We set up the difficulty manager (adjusts questions to your level)
        3. We prepare the quiz flow controller (manages the whole experience)
        """
        # Meet your AI assistant - it creates smart questions
        self.llm_client = GeminiClient()
        
        # This reads the AI's responses and makes sense of them
        self.parser = ResponseParser()
        
        # This decides if your next question should be easier or harder
        self.difficulty_manager = DifficultyManager()
        
        # This holds the instruction templates for the AI
        self.prompt_templates = PromptTemplates()
        
        # The quiz manager orchestrates everything
        self.quiz_manager = QuizManager(
            llm_client=self.llm_client,
            parser=self.parser,
            difficulty_manager=self.difficulty_manager,
            prompt_templates=self.prompt_templates
        )
        
        # Get your quiz ready to go
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """
        This sets up all the memory variables that track your quiz progress.
        Think of it as your personal scorekeeper and progress tracker.
        """
        # These are the things we need to remember about your quiz
        defaults = {
            'quiz_started': False,           # Has the quiz begun?
            'quiz_complete': False,          # Are you finished?
            'subject': None,                 # What are you learning?
            'total_questions': DEFAULT_SETTINGS['total_questions'],  # How many questions?
            'questions_asked': 0,            # How many have you answered?
            'correct_answers': 0,            # Your score! (now computed from history)
            'current_difficulty': DEFAULT_SETTINGS['initial_difficulty'],  # Your current level
            'current_question': None,        # The question you're seeing now
            'answer_submitted': False,       # Have you answered this one?
            'selected_answer': None,         # What did you choose?
            'score_history': [],             # Record of your answers (True/False)
            'difficulty_history': [],        # Record of difficulty changes
            'start_time': None               # When did you start?
        }
        
        # Store all these in the session state (like a temporary memory)
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def render_subject_selection(self):
        """
        This is the welcome screen where you choose what to learn.
        It's like picking a book from the library!
        """
        # Show a friendly welcome header
        st.markdown("""
        <div class="main-header">
            <h1>🧠 Adaptive AI Quiz Generator</h1>
            <p style="font-size: 1.1rem;">Powered by Gemini AI • Difficulty adapts to your performance</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Center the selection panel for a clean look
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.subheader("📚 Select Your Subject")
            
            # Pick what you want to learn about
            subject = st.selectbox(
                "Choose a subject to get started:",
                SUBJECTS,
                help="Select the topic you want to be quizzed on"
            )
            
            # Decide how many questions you want to face
            total_questions = st.slider(
                "Number of questions:",
                min_value=5,
                max_value=15,
                value=10,
                help="Choose how many questions you want to answer (5-15)"
            )
            
            # Choose where you want to start
            starting_difficulty = st.selectbox(
                "Starting difficulty level:",
                DIFFICULTY_LEVELS,
                index=DIFFICULTY_LEVELS.index("Medium"),
                help="Select your preferred starting difficulty"
            )
            
            # Give a helpful hint about how the quiz works
            st.caption(f"📌 You'll start at **{starting_difficulty}** level. Difficulty will adjust based on your answers.")
            
            # The big green button to start your adventure
            if st.button("🚀 Start Quiz", use_container_width=True):
                with st.spinner("🎯 Generating your first question..."):
                    self.quiz_manager.start_quiz(subject, total_questions, starting_difficulty)
                    st.rerun()
    
    def render_active_quiz(self):
        """
        This is where the real action happens!
        You see questions, pick answers, and get instant feedback.
        """
        # Show your progress so far
        display_metrics(
            current_question=st.session_state.questions_asked + 1,
            total_questions=st.session_state.total_questions,
            difficulty=st.session_state.current_difficulty,
            score=st.session_state.correct_answers,
            total_asked=st.session_state.questions_asked
        )
        
        # Show how far you've come with a visual progress bar
        progress = st.session_state.questions_asked / st.session_state.total_questions
        st.progress(progress, text=f"Progress: {int(progress * 100)}%")
        
        st.divider()
        
        # Display the current question
        question_data = st.session_state.current_question
        selected_answer = show_question(
            question_data=question_data,
            disabled=st.session_state.answer_submitted
        )
        
        # If you haven't submitted your answer yet
        if not st.session_state.answer_submitted:
            if st.button("📝 Submit Answer", type="primary", use_container_width=True):
                if selected_answer:
                    st.session_state.selected_answer = selected_answer
                    st.session_state.answer_submitted = True
                    st.rerun()
                else:
                    st.warning("⚠️ Please select an answer first!")
        else:
            # Check if you got it right!
            is_correct = st.session_state.selected_answer == question_data['answer']
            
            # Show you the answer and explanation
            show_explanation(
                is_correct=is_correct,
                correct_answer=question_data['answer'],
                explanation=question_data['explanation']
            )
            
            # Keep track of your performance
            st.session_state.score_history.append(is_correct)
            st.session_state.difficulty_history.append(st.session_state.current_difficulty)
            
            # --- FIX: Compute correct_answers from history ---
            st.session_state.correct_answers = sum(st.session_state.score_history)
            # ------------------------------------------------
            
            # Are you done or should we continue?
            if st.session_state.questions_asked >= st.session_state.total_questions - 1:
                button_label = "🏁 Finish Quiz"
            else:
                button_label = "➡️ Next Question"
            
            # Move to the next question or finish up
            if st.button(button_label, type="primary", use_container_width=True):
                st.session_state.questions_asked += 1
                
                if st.session_state.questions_asked >= st.session_state.total_questions:
                    st.session_state.quiz_complete = True
                else:
                    self.quiz_manager.next_question(is_correct)
                
                st.rerun()
    
    def render_quiz_complete(self):
        """
        Celebrations! You finished the quiz!
        Here's where you see your results and how well you did.
        """
        # Show your final results
        render_results_page(
            correct_answers=st.session_state.correct_answers,
            total_questions=st.session_state.total_questions,
            score_history=st.session_state.score_history,
            difficulty_history=st.session_state.difficulty_history,
            difficulty_levels=DIFFICULTY_LEVELS,
            start_time=st.session_state.start_time
        )
        
        # Want to go again? Here's your chance!
        if st.button("🔄 Take Another Quiz", type="primary", use_container_width=True):
            # Clean up and start fresh
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    def run(self):
        """
        This is the main controller that decides what to show you:
        - The welcome screen if you haven't started
        - The quiz if you're in the middle
        - The results if you've finished
        """
        if not st.session_state.quiz_started:
            self.render_subject_selection()
        elif st.session_state.quiz_complete:
            self.render_quiz_complete()
        else:
            self.render_active_quiz()

# ============================================================
# STEP 3: Let's Go! Launch Your Quiz App
# ============================================================

# This is the entry point - when you run the script, this starts everything
if __name__ == "__main__":
    app = QuizApp()
    app.run()