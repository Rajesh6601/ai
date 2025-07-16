import os
import time
import streamlit as st
from langchain_groq import ChatGroq
from langsmith import traceable

class GroqLLM:
    def __init__(self,user_contols_input):
        self.user_controls_input=user_contols_input

    @traceable(name="get_llm_model")
    def get_llm_model(self, max_retries=3, retry_delay=5):
        """
        Get LLM model with retry logic for service unavailable errors
        """
        for attempt in range(max_retries):
            try:
                groq_api_key=self.user_controls_input["GROQ_API_KEY"]
                selected_groq_model=self.user_controls_input["selected_groq_model"]
                if groq_api_key=='' and os.environ["GROQ_API_KEY"] =='':
                    st.error("Please Enter the Groq API KEY")

                llm=ChatGroq(api_key=groq_api_key,model=selected_groq_model)
                return llm

            except Exception as e:
                # Check for specific Groq API errors
                error_msg = str(e)
                if "503" in error_msg or "Service unavailable" in error_msg:
                    if attempt < max_retries - 1:
                        st.info(f"Groq service unavailable. Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                        time.sleep(retry_delay)
                        continue
                    else:
                        raise ValueError(f"Groq API Service Unavailable (503) after {max_retries} attempts: {error_msg}")
                elif "429" in error_msg:
                    if attempt < max_retries - 1:
                        st.info(f"Rate limit exceeded. Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                        time.sleep(retry_delay)
                        continue
                    else:
                        raise ValueError(f"Groq API Rate Limit Exceeded (429) after {max_retries} attempts: {error_msg}")
                elif "401" in error_msg:
                    raise ValueError(f"Groq API Authentication Error (401): Check your API key")
                else:
                    raise ValueError(f"Error Occurred With Exception : {e}")
        
        # This should never be reached, but just in case
        raise ValueError("Unexpected error in retry logic")