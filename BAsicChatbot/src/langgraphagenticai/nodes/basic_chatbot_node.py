from src.langgraphagenticai.state.state import State
from langsmith import traceable

class BasicChatbotNode:
    """
    Basic Chatbot login implementation
    """
    def __init__(self,model):
        self.llm=model

    @traceable(name="basic_chatbot_process")
    def process(self,state:State)->dict:
        """
        Processes the input state and generates a chatbot response.
        """
        return {"messages":self.llm.invoke(state['messages'])}

