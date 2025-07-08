from src.langgraphagenticai.state.state import State

class ChatbotWithToolNodes:
    def __init__(self, model):
        self.llm = model
    
    def process(self, state: State)-> dict:
        """
        Process the input state and generates a response with tool intergration
        """
        user_input = state['messages'][-1] if state['messages'] else ''
        llm_response = self.llm.invoke([{'role':'user', 'content':user_input}])

        #stimulate the tools specific logic
        tools_response = f'Tool intergartion for : {user_input}'

        return {'messages': [llm_response, tools_response]}

    def create_chatbot(self, tools):
        """
        Returns a chatbot node function
        """ 
        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state = State):
            """
            Chatbot logic for processing the input state and returning a response.
            """
            return {'messages': llm_with_tools.invoke(State['messages'])}
        
        return chatbot_node
