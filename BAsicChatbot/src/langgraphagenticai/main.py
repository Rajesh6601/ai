import streamlit as st
from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMS.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlitui.display_result import DisplayResultStreamlit
from src.langgraphagenticai.utils.service_status import ServiceStatusChecker
from src.langgraphagenticai.utils.langsmith_config import setup_langsmith
from src.langgraphagenticai.utils.langsmith_monitor import LangSmithMonitor
from dotenv import load_dotenv
from langsmith import traceable

# Load environment variables
load_dotenv()

# Initialize LangSmith for debugging and monitoring
langsmith_enabled = setup_langsmith()
monitor = LangSmithMonitor()

@traceable(name="langgraph_agenticai_app")
def load_langgraph_agenticai_app():
    """
    Loads and runs the LangGraph AgenticAI application with Streamlit UI.
    This function initializes the UI, handles user input, configures the LLM model,
    sets up the graph based on the selected use case, and displays the output while 
    implementing exception handling for robustness. Now includes chat memory support.
    """

    # Initialize session state for chat history and thread ID
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "thread_id" not in st.session_state:
        import uuid
        st.session_state.thread_id = str(uuid.uuid4())

    ##Load UI
    ui=LoadStreamlitUI()
    user_input=ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return
    
    # Add LangSmith monitoring sidebar
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🔍 LangSmith Monitoring")
        
        if langsmith_enabled:
            st.success("✅ LangSmith Enabled")
            config = monitor.get_monitoring_config()
            
            # Dashboard links
            st.markdown(f"🔗 [Dashboard]({config['dashboard_url']})")
            st.markdown(f"📈 [Traces]({config['traces_url']})")
            st.markdown(f"📊 [Analytics]({config['analytics_url']})")
            
            # Show traced components
            with st.expander("📋 Traced Components"):
                for component in config['traced_components']:
                    st.write(f"• {component}")
        else:
            st.warning("⚠️ LangSmith Not Configured")
            st.info("Add LANGSMITH_API_KEY to .env file to enable monitoring")
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    user_message = st.chat_input("Enter your message:")

    if user_message:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_message})
        
        # Display user message
        with st.chat_message("user"):
            st.write(user_message)
        
        try:
            ## Configure The LLM's
            obj_llm_config=GroqLLM(user_contols_input=user_input)
            model=obj_llm_config.get_llm_model()

            if not model:
                st.error("Error: LLM model could not be initialized")
                return
            
            # Initialize and set up the graph based on use case
            usecase=user_input.get("selected_usecase")

            if not usecase:
                    st.error("Error: No use case selected.")
                    return
            
            ## Graph Builder
            graph_builder=GraphBuilder(model)
            try:
                 graph=graph_builder.setup_graph(usecase)
                 print(user_message)
                 DisplayResultStreamlit(usecase, graph, user_message, st.session_state.thread_id).display_result_on_ui()
            except Exception as e:
                 error_msg = str(e)
                 if "503" in error_msg or "Service unavailable" in error_msg:
                     st.error("🚨 **Groq API Service Unavailable**")
                     st.warning("The Groq API service is temporarily down. This is a service-side issue, not a problem with your code.")
                     
                     # Add service status check button
                     col1, col2 = st.columns(2)
                     with col1:
                         if st.button("🔄 Check Service Status", key="inner_status_check"):
                             ServiceStatusChecker.display_service_status()
                     with col2:
                         if st.button("📊 View Full Status Page", key="inner_status_page"):
                             st.markdown("[Open Groq Status Page](https://groqstatus.com/)")
                             
                     st.info("**What you can do:**")
                     st.info("• Wait a few minutes and try again")
                     st.info("• Check service status at: https://groqstatus.com/")
                     st.info("• The Groq team is working on a fix")
                 else:
                     st.error(f"Error: Graph set up failed- {e}")
                 return

        except Exception as e:
             error_msg = str(e)
             if "503" in error_msg or "Service unavailable" in error_msg:
                 st.error("🚨 **Groq API Service Unavailable**")
                 st.warning("The Groq API service is temporarily down. This is a service-side issue, not a problem with your code.")
                 
                 # Add service status check button
                 col1, col2 = st.columns(2)
                 with col1:
                     if st.button("🔄 Check Service Status"):
                         ServiceStatusChecker.display_service_status()
                 with col2:
                     if st.button("📊 View Full Status Page"):
                         st.markdown("[Open Groq Status Page](https://groqstatus.com/)")
                         
                 st.info("**What you can do:**")
                 st.info("• Wait a few minutes and try again")
                 st.info("• Check service status at: https://groqstatus.com/")
                 st.info("• The Groq team is working on a fix")
             else:
                 st.error(f"Error: Graph set up failed- {e}")
             return
