from src.langgraphagenticai.state.state import State

class BasicChatbotNode:
    """
    Basic Chatbot login imnplementation
    """

    def __init__(self,model):
        self.llm=model

    def process(self,state:State):
        """
        Process the input state and generate a chatbot reponse.
        """

        return {"messages":self.llm.invoke(state["messages"])}
