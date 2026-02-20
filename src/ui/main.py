import streamlit as st
import os
from src.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMS.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.ui.streamlitui.display_result import DisplayResultStreamlit
from src.utils.logger import setup_logger

# Initialize Logger
logger = setup_logger(__name__)

def load_langgraph_agenticai_ui():
    """
    Loads and runs the LangGraph AgenticAI application with Streamlit UI.
    This function initializes the UI, handles user input, configures the LLM model,
    sets up the graph based on the selected use case, and displays the output while
    implementing exception handling for robustness.
    """

    ## Load UI
    try:
        ui = LoadStreamlitUI()
        user_input = ui.streamlit_load_ui()
    except Exception as e:
        logger.error(f"Failed to load UI: {str(e)}")
        st.error("Error: Failed to load UI components.")
        return

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if not user_input:
        # This might be normal if the user hasn't selected anything yet, 
        # but if it returns None it implies an error in load_ui logic usually.
        # Assuming load_ui returns dict, empty dict is "falsy" but might be valid state.
        # But looking at loadui.py, it returns self.user_controls.
        logger.warning("User input not fully loaded or empty.")
        # st.error("Error: Failed to load user input from the UI.") # Optional depending on flow
        return
        
    user_message = st.chat_input("Enter your message here:")

    if user_message:
        logger.info(f"User message received: {user_message}")
        try:
            # Configure the LLM
            try:
                obj_llm_config = GroqLLM(user_controls_input=user_input)
                model = obj_llm_config.get_llm_model()
            except Exception as e:
                logger.error(f"LLM Configuration failed: {str(e)}")
                st.error(f"Error: LLM Configuration failed: {str(e)}")
                return

            if not model:
                logger.error("LLM model could not be initialized (returned None).")
                st.error("Error: LLM model could not be initialized.")
                return

            # Initialize and set up the graph based on the use case
            usecase = user_input.get("selected_usecase")
            if not usecase:
                logger.error("No use case selected.")
                st.error("Error: No use case selected.")
                return
            
            logger.info(f"Selected usecase: {usecase}")

            ## Graph Builder
            try:
                if usecase == "Chatbot with Tool":
                    tavily_key = user_input.get("TAVILY_API_KEY") or os.getenv("TAVILY_API_KEY", "")
                    if not tavily_key:
                        logger.error("TAVILY_API_KEY is missing.")
                        st.error("Error: TAVILY_API_KEY is missing. Enter it in the sidebar or set env var.")
                        return
                    os.environ["TAVILY_API_KEY"] = tavily_key
                graph_builder = GraphBuilder(model)
                graph = graph_builder.setup_graph(usecase)
                logger.info("Graph setup successful.")
                
                DisplayResultStreamlit(usecase, graph, user_message).display_result_on_ui()

            except Exception as e:
                logger.error(f"Graph execution failed: {str(e)}")
                st.error(f"Error: Graph execution failed: {str(e)}")
                return
        except Exception as e:
            logger.exception(f"An unexpected error occurred: {str(e)}")
            st.error(f"An error occurred: {str(e)}")
            return
