import streamlit as st

from src.ui.uiconfigfile import Config


class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def _apply_custom_theme(self):
        st.markdown(
            """
            <style>
            :root {
                --bg: #090d14;
                --panel: #101725;
                --panel-2: #0f172a;
                --text: #e2e8f0;
                --muted: #94a3b8;
                --border: #1f2937;
                --primary: #38bdf8;
            }
            .stApp {
                background: radial-gradient(1200px 600px at 80% -10%, #0b1b37 0%, var(--bg) 50%);
                color: var(--text);
            }
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #111827 0%, #0f172a 100%);
                border-right: 1px solid var(--border);
            }
            [data-testid="stSidebar"] * {
                color: var(--text);
            }
            .app-hero {
                background: linear-gradient(90deg, rgba(56,189,248,0.12), rgba(14,165,233,0.03));
                border: 1px solid rgba(56,189,248,0.2);
                border-radius: 14px;
                padding: 16px 18px;
                margin: 4px 0 14px 0;
            }
            .app-title {
                margin: 0;
                font-size: clamp(1.5rem, 2.3vw, 2.4rem);
                font-weight: 700;
                letter-spacing: 0.2px;
                color: #f8fafc;
            }
            .app-subtitle {
                margin-top: 6px;
                font-size: 0.95rem;
                color: var(--muted);
            }
            .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
                background: #0b1220 !important;
                border-color: #1e293b !important;
            }
            .stChatInputContainer {
                border-top: 1px solid #1f2937;
                background: rgba(15,23,42,0.75);
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

    def streamlit_load_ui(self):
        title = self.config.get_page_title()
        st.set_page_config(page_title=title, layout="wide")
        st.session_state.timeframe=''
        st.session_state.IsFetchButtonClicked=False
        self._apply_custom_theme()

        st.markdown(
            f"""
            <div class="app-hero">
                <h1 class="app-title">{title}</h1>
                <div class="app-subtitle">Agentic workflows with configurable models and use cases.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.sidebar:
            st.header("Configuration Options")
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            self.user_controls["selected_llm"] = st.selectbox("Select LLM Model:", llm_options)

            if self.user_controls["selected_llm"] == "Groq":
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox(
                    "Select GROQ Model:", model_options
                )

                if "Groq_Api_Key" not in st.session_state:
                    st.session_state["Groq_Api_Key"] = ""

                self.user_controls["Groq_Api_Key"] = st.text_input(
                    "API key", type="password", value=st.session_state["Groq_Api_Key"]
                )
                st.session_state["Groq_Api_Key"] = self.user_controls["Groq_Api_Key"]

                if not self.user_controls["Groq_Api_Key"]:
                    st.warning("Please enter your GROQ API key to proceed.")

            self.user_controls["selected_usecase"] = st.selectbox(
                "Select Usecases:", usecase_options
            )
            if self.user_controls["selected_usecase"] in ["Chatbot with Tool", "AI News"]:
                self.user_controls["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"] = st.text_input(
                    "TAVILY_API_KEY", type="password"
                )
                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("Please enter your TAVILY API key to proceed.")

            if self.user_controls["selected_usecase"] == "AI News":
                st.subheader("AI News Explorer")
                time_frame = st.selectbox("Select Time Frame", ["Daily", "Weekly", "Monthly"], index=0)
                if st.button("Fetch Latest AI News", use_container_width=True):
                    st.session_state,IsFetchButtonClicked=True
                    st.session_state["news_time_frame"] = time_frame

            if "messages" in st.session_state and st.sidebar.button("Clear Chat History"):
                st.session_state.messages = []

        return self.user_controls
