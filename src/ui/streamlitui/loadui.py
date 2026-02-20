import streamlit as st
import os

from src.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls={}

    def streamlit_load_ui(self):
        st.set_page_config(page_title=self.config.get_page_title(), layout="wide")
        st.header("LangGraph: Build Stateful Agentic AI LangGraph")
        st.title(self.config.get_page_title())

        with st.sidebar:
            st.header("Configuration Options")
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()
           
            # LLM Selection
            self.user_controls['selected_llm'] = st.selectbox(
                "Select LLM Model:",
                llm_options
            )

            if self.user_controls['selected_llm'] == "Groq":
                model_options = self.config.get_groq_model_options()
                self.user_controls['selected_groq_model'] = st.selectbox(
                    "Select GROQ Model:",model_options
                
                )

                if "Groq_Api_Key" not in st.session_state:
                    st.session_state["Groq_Api_Key"] = ""
                
                self.user_controls["Groq_Api_Key"] = st.text_input("API key", type="password", value=st.session_state["Groq_Api_Key"])
                st.session_state["Groq_Api_Key"] = self.user_controls["Groq_Api_Key"]

                #validate API Key
                if not self.user_controls["Groq_Api_Key"]:
                    st.warning("Please enter your GROQ API key to proceed.")
                

            ## Usecase Selection
            self.user_controls['selected_usecase'] = st.selectbox("Select Usecases:", usecase_options)
            if self.user_controls["selected_usecase"]=="Chatbot with Tool":
                self.user_controls["TAVILY_API_KEY"] =st.session_state["TAVILY_API_KEY"]=st.text_input("TAVILY_API_KEY", type="password")
                #validate API Key
                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("Please enter your TAVILY API key to proceed.")
            
            if "messages" in st.session_state and st.sidebar.button("Clear Chat History"):
                st.session_state.messages = []
        return self.user_controls
