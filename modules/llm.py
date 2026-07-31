# modules/llm.py - How Your App Talks to Gemini AI
"""
This module is like your personal messenger to Gemini AI.
It handles all the communication with the AI model that generates
your quiz questions.

Think of it as a translator between your app and the powerful
Gemini AI brain!
"""

import google.generativeai as genai
import streamlit as st
import os

class GeminiClient:
    """
    Your friendly AI communicator!
    
    This class knows how to:
    1. Find your secret API key (safely stored)
    2. Connect to Gemini AI
    3. Send questions and get intelligent responses
    """
    
    def __init__(self):
        """
        Setting up the connection to Gemini AI.
        
        This is like picking up the phone and dialing the AI's number.
        We need your API key (like a password) to make the connection.
        """
        try:
            # First, check if we're on the cloud (Streamlit Secrets)
            api_key = st.secrets["GEMINI_API_KEY"]
        except:
            # If not, look for the key in your local environment file
            api_key = os.getenv("GEMINI_API_KEY")
        
        # Safety check: Make sure we have a key
        if not api_key:
            raise ValueError("🔑 GEMINI_API_KEY not found. Please check your secrets or .env file.")
        
        # Configure the connection to Gemini
        genai.configure(api_key=api_key)
        
        # Choose which AI model to use (gemini-pro is great for text)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate_content(self, prompt: str) -> str:
        """
        Send a message to Gemini and get a response.
        
        This is like asking a question to a very smart friend.
        You give them instructions (the prompt) and they give you
        a thoughtful answer.
        
        Args:
            prompt: Your instructions or question for the AI
            
        Returns:
            str: The AI's response (usually a question in JSON format)
        """
        try:
            # Ask Gemini for help
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            # If something goes wrong, let the user know
            st.error(f"⚠️ Oops! Something went wrong with the AI: {str(e)}")
            raise