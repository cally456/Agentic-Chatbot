import os
import streamlit as st 
from langchain_groq import ChatGroq

class GroqLLM:
    def __init__(self,user_controls_input):
        self.user_controls_input = user_controls_input
    
    def get_llm_model(self):
        try:
            groq_api_key = self.user_controls_input.get("Groq_Api_Key") or os.getenv("GROQ_API_KEY", "")
            selected_groq_model = self.user_controls_input.get("selected_groq_model", "")

            deprecated_map = {
                "llama3-8b-8192": "llama-3.1-8b-instant",
                "llama3-70b-8192": "llama-3.1-70b-versatile",
                "gemma2-9b-it": "llama-3.1-8b-instant",
            }
            if selected_groq_model in deprecated_map:
                replacement = deprecated_map[selected_groq_model]
                st.info(
                    f"Selected model '{selected_groq_model}' is deprecated. "
                    f"Using recommended replacement '{replacement}'."
                )
                selected_groq_model = replacement

            if not groq_api_key:
                raise ValueError(
                    "GROQ API key is missing. Set it in the sidebar or GROQ_API_KEY env var."
                )

            llm = ChatGroq(api_key=groq_api_key, model_name=selected_groq_model)
        except Exception as e:
            raise ValueError(f"An error occurred while initializing the Groq LLM: {str(e)}")    
        return llm
