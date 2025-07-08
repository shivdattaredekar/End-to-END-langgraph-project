import os
import streamlit as st
from datetime import date

from langchain_core.messages import AIMessage, HumanMessage
from src.langgraphagenticai.UI.uiconfigfile import Config


class LoadSstreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def initialize_session(self):
        return {
            'current_step': 'requirements',
            "requirements": "",
            "user_stories": "",
            "po_feedback": "",
            "generated_code": "",
            "review_feedback": "",
            "decision": None
        }
    
    def load_streamlit_ui(self):
        st.set_page_config(page_title= "🤖 " + self.config.get_page_title(), layout="wide")
        st.header("🤖 " + self.config.get_page_title())
        st.session_state.timeframe = ''
        st.session_state.IsFetchButtonClicked = False
        st.session_state.IsSDLC = False

        with st.sidebar:
            # Get options from config
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            # LLM selection
            self.user_controls['selected_llm'] = st.selectbox('Select LLM', llm_options)

            if self.user_controls['selected_llm'] == 'Groq':
                # Model selection
                model_options = self.config.get_groq_model_options()
                self.user_controls['selected_groq_model'] = st.selectbox('Select_Model', model_options)
                
                # API key input
                self.user_controls['GROQ_API_KEY'] = st.session_state['GROQ_API_KEY'] = st.text_input('API Key', type='password')

                # Validate API key
                if not self.user_controls['GROQ_API_KEY']:
                    st.warning("⚠️ Please enter your GROQ API key to proceed. Don't have? refer : https://console.groq.com/keys ")
                   
            # Usecase selection
            self.user_controls['usecase_options'] = st.selectbox('Select_Usecase', usecase_options)

            if self.user_controls['usecase_options'] == 'Chatbot with Tool' or self.user_controls['usecase_options'] == 'AI News':
                # API key input
                os.environ['TAVILY_API_KEY'] = self.user_controls['TAVILY_API_KEY'] = st.session_state['TAVILY_API_KEY'] = st.text_input('TAVILY_API_KEY', type='password')

                # Validate the API key
                if not self.user_controls['TAVILY_API_KEY']:
                    st.warning("⚠️ Please enter your TAVILY_API_KEY key to proceed. Don't have? refer : https://app.tavily.com/home")

                elif self.user_controls['usecase_options'] == 'AI News':
                    st.subheader("📰 AI News Explorer ")

                    with st.sidebar:
                        timeframe = st.selectbox(
                                "📅 Select Time Frame",
                        ["Daily", "Weekly", "Monthly"],
                        index=0
                    )

                    if st.button("🔍 Fetch Latest AI News", use_container_width=True):
                        st.session_state.IsFetchButtonClicked = True
                        st.session_state.timeframe = timeframe
                    else :
                        st.session_state.IsFetchButtonClicked = False

            if 'state' not in st.session_state:
                st.session_state.state = self.initialize_session() 

        














