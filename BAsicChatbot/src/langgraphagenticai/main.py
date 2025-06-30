import streamlit as st
from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMS.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlitui.display_result import DisplayResultStreamlit

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
                 st.error(f"Error: Graph set up failed- {e}")
                 return

        except Exception as e:
             st.error(f"Error: Graph set up failed- {e}")
             return
