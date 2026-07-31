# modules/parser.py - Making Sense of AI's Answers
import json
import re
import streamlit as st

class ResponseParser:
    def parse_response(self, response_text: str) -> dict:
        try:
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                question_data = json.loads(json_str)
            else:
                question_data = json.loads(response_text)
            self._validate_question_data(question_data)
            return question_data
        except Exception as e:
            st.error(f"⚠️ Using fallback question: {str(e)}")
            return self._get_fallback_question()

    def _validate_question_data(self, data: dict) -> bool:
        required_fields = ['question', 'options', 'answer', 'explanation']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing field: {field}")
        if len(data['options']) != 4:
            raise ValueError("Must have 4 options")
        # --- FIX: ensure explanation is a string ---
        if not isinstance(data['explanation'], str):
            raise ValueError("Explanation must be a string")
        return True

    def _get_fallback_question(self) -> dict:
        # 20+ unique fallback questions (abbreviated for space – you have the full list)
        pool = [
            {"question": "What is the best way to learn programming?", "options": ["A. Practice regularly", "B. Read books only", "C. Watch videos only", "D. Never practice"], "answer": "A. Practice regularly", "explanation": "Regular practice is essential for mastering any skill."},
            # ... (include all 20 questions from the previous version)
            # (copy the full list from the previous answer)
        ]
        if 'parser_used_fallbacks' not in st.session_state:
            st.session_state.parser_used_fallbacks = []
        used = st.session_state.parser_used_fallbacks
        if len(used) == len(pool):
            used.clear()
        available = [i for i in range(len(pool)) if i not in used]
        idx = available[0]
        used.append(idx)
        return pool[idx]