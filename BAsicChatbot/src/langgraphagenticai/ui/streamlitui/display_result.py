import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage
import json


class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message, thread_id):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message
        self.thread_id = thread_id

    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message
        thread_id = self.thread_id
        
        print(f"Processing message: {user_message}")
        print(f"Thread ID: {thread_id}")
        
        if usecase == "Basic Chatbot":
            # Create config with thread_id for memory persistence
            config = {"configurable": {"thread_id": thread_id}}
            
            # Stream the graph with memory support
            for event in graph.stream({'messages': [("user", user_message)]}, config):
                print(event.values())
                for value in event.values():
                    if 'messages' in value:
                        # Handle both single message and list of messages
                        messages = value['messages']
                        if not isinstance(messages, list):
                            messages = [messages]
                        
                        # Get the latest AI message
                        for message in messages:
                            if hasattr(message, 'content') and message.content and hasattr(message, 'type'):
                                # Check if it's an AI message (not user message)
                                if message.type == 'ai' or str(type(message).__name__) == 'AIMessage':
                                    # Display assistant response
                                    with st.chat_message("assistant"):
                                        st.write(message.content)
                                    
                                    # Add assistant message to session state
                                    st.session_state.messages.append({
                                        "role": "assistant", 
                                        "content": message.content
                                    })
                                    break
