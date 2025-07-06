import streamlit as st
import os

from src.langgraphagenticai.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        try:
            self.config = Config()
        except Exception as e:
            st.error(f"Error loading configuration: {e}")
            # Create a minimal config with defaults
            self.config = None
        self.user_controls = {}

    def load_streamlit_ui(self):
        # Get page title with multiple fallback layers
        try:
            if self.config:
                page_title = self.config.get_page_title()
            else:
                page_title = None
        except Exception as e:
            st.error(f"Error getting page title: {e}")
            page_title = None
        
        # Ensure page_title is never None
        if not page_title or page_title is None:
            page_title = "LangGraph Chatbot"
        
        # Additional safety check
        if not isinstance(page_title, str):
            page_title = "LangGraph Chatbot"
        
        try:
            st.set_page_config(page_title="🤖 " + page_title, layout="wide")
            st.header("🤖 " + page_title)
        except Exception as e:
            st.error(f"Error setting page config: {e}")
            # Fallback without emoji if there are encoding issues
            st.set_page_config(page_title=page_title, layout="wide")
            st.header(page_title)


        with st.sidebar:
            # Get options from config with fallbacks
            try:
                if self.config:
                    llm_options = self.config.get_llm_options()
                    usecase_options = self.config.get_usecase_options()
                else:
                    llm_options = ["Groq"]
                    usecase_options = ["Basic Chatbot"]
            except Exception as e:
                st.error(f"Error loading config options: {e}")
                llm_options = ["Groq"]
                usecase_options = ["Basic Chatbot"]

            # LLM selection
            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)

            if self.user_controls["selected_llm"] == 'Groq':
                # Model selection
                try:
                    if self.config:
                        model_options = self.config.get_groq_model_options()
                    else:
                        model_options = ["llama3-8b-8192", "llama3-70b-8192", "gemma2-9b-it"]
                except Exception as e:
                    st.error(f"Error loading model options: {e}")
                    model_options = ["llama3-8b-8192", "llama3-70b-8192", "gemma2-9b-it"]
                
                self.user_controls["selected_groq_model"] = st.selectbox("Select Model", model_options)
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"]=st.text_input("API Key",type="password")
                # Validate API key
                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("⚠️ Please enter your GROQ API key to proceed. Don't have? refer : https://console.groq.com/keys ")
            
            ## USecase selection
            self.user_controls["selected_usecase"]=st.selectbox("Select Usecases",usecase_options)

            if self.user_controls["selected_usecase"] == 'Chatbot With Web':
                os.environ["TAVILY_API_KEY"]=self.user_controls["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"]=st.text_input("TAVILY API Key",type="password")
            
             # Validate API key
                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("⚠️ Please enter your TAVILY API key to proceed. Don't have? refer : https://app.tavily.com/home ")

            # Add Clear Chat button
            st.markdown("---")
            if st.button("🗑️ Clear Chat History", type="secondary"):
                st.session_state.messages = []
                import uuid
                st.session_state.thread_id = str(uuid.uuid4())
                st.rerun()

        return self.user_controls
