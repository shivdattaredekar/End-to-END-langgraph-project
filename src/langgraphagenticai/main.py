import streamlit as st

from src.langgraphagenticai.UI.streamlitUI.loadUI import  LoadStreamlitUI
from src.langgraphagenticai.llms.groqllm import GroqLLM
from src.langgraphagenticai.graphs.graph_builder import GraphBuilder
from src.langgraphagenticai.UI.streamlitUI.display_result import DisplayResultStreamlit

# Main function start

def load_langgraph_agenticai_app():
    """
    Loads and runs the LangGraph AgenticAI application with Streamlit UI.
    This function initializes the UI, handles user input, configures the LLM model,
    sets up the graph based on the selected use case, and displays the output while 
    implementing exception handling for robustness.
    """
    # Load UI
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return
    
    # Text input for the user message
    if st.session_state.IsFetchButtonClicked:
        user_message = st.session_state.timeframe
    else:
        user_message= st.chat_input('Enter your message:')

    if user_message:
        try:
            obj_llm_config = GroqLLM(user_controls_input=user_input)
            model = obj_llm_config.get_llm_model()

            if not model:
                st.error('Error: No use case selected.')
                return
            
            # Initialize and setup the graph based on usecase
            usecase=user_input.get('selected_usecase')
            
            # Graph builder
            graph_builer = GraphBuilder(model=model)
            try:
                graph = graph_builer.setup_graph(usecase=usecase)
                DisplayResultStreamlit(usecase,graph,user_message).display_result_on_ui()

            except Exception as e:
                st.error(f'Error: Graph setup failed {e}')
                return
            
        except Exception as e:
            raise ValueError(f'Error occured with Exception:{e}')
        


















