# utils/helpers.py - Reusable UI Components
"""
This is your toolkit of helpful functions that make the user interface
look great and work smoothly.

Think of these as building blocks that you can mix and match
to create the perfect quiz experience!
"""

import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

# Local imports (NO circular import here)
from utils.constants import DIFFICULTY_COLORS, MESSAGES, PERFORMANCE


def display_metrics(current_question: int, total_questions: int, 
                   difficulty: str, score: int, total_asked: int):
    """
    Show your progress in a clean, visual dashboard.
    """
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="📝 Question",
            value=f"{current_question}/{total_questions}"
        )
    with col2:
        color = DIFFICULTY_COLORS.get(difficulty, "#888888")
        st.markdown(f"""
        <div style='text-align: center;'>
            <div style='font-size: 14px; color: #888;'>🎯 Difficulty</div>
            <div style='font-size: 24px; font-weight: bold; color: {color};'>
                {difficulty}
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.metric(
            label="⭐ Score",
            value=f"{score}/{total_asked if total_asked > 0 else 0}"
        )
    with col4:
        if st.session_state.get('start_time'):
            elapsed = (datetime.now() - st.session_state.start_time).total_seconds()
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            st.metric("⏱️ Time", f"{minutes}m {seconds}s")


def show_question(question_data: dict, disabled: bool):
    """
    Display a question with its answer options.
    """
    st.subheader(f"📝 {question_data['question']}")
    options = question_data['options']
    selected = st.radio(
        "Choose your answer:",
        options,
        key="answer_radio",
        disabled=disabled,
        index=None
    )
    return selected


def show_explanation(is_correct: bool, correct_answer: str, explanation: str):
    """
    Show feedback after you submit your answer.
    """
    st.divider()
    st.subheader("📚 Explanation")
    if is_correct:
        st.success("✅ Correct! Well done!")
    else:
        st.error(f"❌ Incorrect. The correct answer was: {correct_answer}")
    
    # --- REMOVED background-color to make it transparent ---
    st.markdown(f"""
    <div style='padding: 1rem; border-radius: 10px; margin: 1rem 0;'>
        <strong>💡 Explanation:</strong><br>
        {explanation}
    </div>
    """, unsafe_allow_html=True)


def get_performance_message(percentage: float) -> tuple:
    """
    Get an encouraging message based on your score.
    """
    if percentage >= PERFORMANCE['excellent']:
        return MESSAGES['excellent'], 'success'
    elif percentage >= PERFORMANCE['good']:
        return MESSAGES['good'], 'info'
    else:
        return MESSAGES['needs_improvement'], 'warning'


def render_results_page(correct_answers: int, total_questions: int, 
                       score_history: list, difficulty_history: list,
                       difficulty_levels: list, start_time: datetime):
    """
    Show your complete results after finishing the quiz.
    """
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='font-size: 3rem;'>🎉 Quiz Complete!</h1>
    </div>
    """, unsafe_allow_html=True)
    
    percentage = (correct_answers / total_questions) * 100
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 Score", f"{correct_answers}/{total_questions}")
    with col2:
        st.metric("🎯 Accuracy", f"{percentage:.1f}%")
    with col3:
        # Compute average difficulty using the provided difficulty_levels list
        if difficulty_history:
            indices = [difficulty_levels.index(d) for d in difficulty_history]
            avg_index = sum(indices) / len(indices)
            rounded = round(avg_index)
            rounded = max(0, min(rounded, len(difficulty_levels) - 1))
            avg_diff = difficulty_levels[rounded]
            st.metric("📈 Avg Difficulty", avg_diff)
        else:
            st.metric("📈 Avg Difficulty", "N/A")
    with col4:
        if start_time:
            elapsed = (datetime.now() - start_time).total_seconds()
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            st.metric("⏱️ Time", f"{minutes}m {seconds}s")
    
    st.divider()
    
    message, msg_type = get_performance_message(percentage)
    if msg_type == 'success':
        st.success(message)
        st.balloons()
    elif msg_type == 'info':
        st.info(message)
    else:
        st.warning(message)
    
    # Difficulty progression chart
    if difficulty_history:
        st.subheader("📈 Difficulty Progression")
        
        fig, ax = plt.subplots(figsize=(12, 4))
        # Convert difficulty to indices using the passed difficulty_levels
        diff_indices = [difficulty_levels.index(d) for d in difficulty_history]
        questions = range(1, len(diff_indices) + 1)
        
        ax.plot(questions, diff_indices, marker='o', linewidth=2, markersize=10, color='#667eea')
        ax.set_yticks(range(len(difficulty_levels)))
        ax.set_yticklabels(difficulty_levels)
        ax.set_xlabel("Question Number", fontsize=12)
        ax.set_ylabel("Difficulty Level", fontsize=12)
        ax.set_title("How Difficulty Adapted During Your Quiz", fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        for i, (q, diff_idx) in enumerate(zip(questions, diff_indices)):
            is_correct = score_history[i] if i < len(score_history) else False
            color = '#4CAF50' if is_correct else '#F44336'
            ax.scatter(q, diff_idx, color=color, s=200, zorder=5, edgecolor='white', linewidth=2)
        
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#4CAF50', label='✅ Correct Answer'),
            Patch(facecolor='#F44336', label='❌ Incorrect Answer'),
            Patch(facecolor='#667eea', label='Difficulty Level')
        ]
        ax.legend(handles=legend_elements, loc='upper left')
        st.pyplot(fig)
    
    with st.expander("📋 View Detailed Results"):
        for i, (correct, diff) in enumerate(zip(score_history, difficulty_history)):
            status = "✅ Correct" if correct else "❌ Incorrect"
            st.write(f"**Q{i+1}**: {status} at *{diff}* level")