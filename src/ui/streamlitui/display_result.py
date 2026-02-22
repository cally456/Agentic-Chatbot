import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import json


class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message
        assistant_text = ""
        
        # Display user message first
        with st.chat_message("user"):
            st.markdown(user_message)
        
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": user_message})

        if usecase == "Basic Chatbot":
            with st.chat_message("assistant"):
                # Container for streaming output
                response_container = st.empty()
                
                final_response = ""
                
                # Use stream to get incremental updates if the LLM supports it, 
                # though LangGraph stream output granularity depends on the node.
                # Here we are iterating over graph events.
                for event in graph.stream({'messages': [("user", user_message)]}):
                    for value in event.values():
                        # value['messages'] is the result from the node.
                        message = value['messages']
                        if hasattr(message, 'content'):
                            final_response = message.content
                            response_container.markdown(final_response)
                        else:
                            # Fallback if it's a list or something else
                            final_response = str(message)
                            response_container.write(final_response)
            st.session_state.messages.append({"role": "assistant", "content": final_response})
        elif usecase in ["Chatbot with Tool", "Basic Chatbot with Tools"]:
            # Handle tool use cases
            initial_state ={"messages":[("user", user_message)]}
            res = graph.invoke(initial_state)
            for message in res['messages']:
                if type(message)== HumanMessage:
                    with st.chat_message("user"):
                        st.write(message.content)
                elif type(message)==ToolMessage:
                    with st.chat_message("ai"):
                        st.write("Tool Call Start")
                        st.write(message.content)
                        st.write("Tool Call End")
                elif type(message)==AIMessage and message.content:
                    with st.chat_message("assistant"):
                        st.write(message.content)
                        assistant_text = message.content
            if assistant_text:
                st.session_state.messages.append({"role": "assistant", "content": assistant_text})

        elif usecase=="AI News":
            frequency = st.session_state.get("news_time_frame", "Daily")
            with st.spinner(f"Fetching and summarizing {frequency} AI news..."):
                result = graph.invoke({
                    "messages": [{"role":"user","content": user_message}],
                    "frequency": frequency,
                    "query": user_message
                })
                try:
                    AI_News_Path = f"./AINews/{frequency.lower()}_ai_news_summary.md"
                    with open(AI_News_Path, "r") as file:
                        summary_content = file.read()
                        
                        st.markdown(summary_content, unsafe_allow_html=True )
                        assistant_text = summary_content
                except FileNotFoundError:
                    st.error(f"News Not Generated or File not found: {AI_News_Path}")
                except Exception as e:
                    st.error(f"Error displaying AI news: {e}")
            if assistant_text:
                st.session_state.messages.append({"role": "assistant", "content": assistant_text})
