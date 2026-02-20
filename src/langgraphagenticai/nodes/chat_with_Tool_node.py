from src.langgraphagenticai.state.state import State

"""Chatbot logic enhanced with toool integration."""

class ChatbotWithToolNode:
    def __init__(self,llm):
        self.llm=llm

    def process(self,state:State)->dict:
        """Processes the input state and generates a chatbot response."""

        user_input =state["messages"][-1]if state["messages"] else ""
        llm_response = self.llm.invoke([{"role":"user","content":user_input}])

        #Simulate tool specific logic 

        tools_reponse = f"Tool integeration for: '{user_input}'"

        return {"messages":[llm_response,tools_reponse]}
    
    def create_chatbot(self,tools):
        """Returns a chatbot node function."""
        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state:State):
            """
           Chatbot logic for processsing the input state and returning a reponse.  """
            
            return {"messages":[llm_with_tools.invoke(state["messages"])]}
        return chatbot_node
            
