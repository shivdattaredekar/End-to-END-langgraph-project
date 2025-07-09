from langgraph.graph import START, END, MessagesState, StateGraph
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_core.prompts import ChatPromptTemplate

from src.langgraphagenticai.llms.groqllm import GroqLLM
from src.langgraphagenticai.nodes.ai_news_node import AINewsNode
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraphagenticai.nodes.chatbot_with_tool_node import ChatbotWithToolNodes
from src.langgraphagenticai.state.state import State
from src.langgraphagenticai.tools.search_tool import get_tools, create_tool_node



class GraphBuilder:
    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)

    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot graph using LangGraph.
        This method initializes a chatbot node using the `BasicChatbotNode` class 
        and integrates it into the graph. The chatbot node is set as both the 
        entry and exit point of the graph.
        """
        self.basic_chatbot_node = BasicChatbotNode(self.llm)
        self.graph_builder.add_node('Chatbot',self.basic_chatbot_node)
        self.graph_builder.add_edge(START, 'Chatbot')
        self.graph_builder.add_edge('Chatbot', END)
        
    def ai_news_build_graph(self):
        # Initialize the AINewsNode
        ai_news_node= AINewsNode(self.llm)

        self.graph_builder.add_node("fetch_news", ai_news_node.fetch_news)
        self.graph_builder.add_node("summarize_news", ai_news_node.summarize_news)
        self.graph_builder.add_node("save_result", ai_news_node.save_result)

        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news", "summarize_news")
        self.graph_builder.add_edge("summarize_news", "save_result")
        self.graph_builder.add_edge("save_result", END)


    def chatbot_with_tools_build_graph(self):
        """
        Builds an advanced chatbot graph with tool integration.
        This method creates a chatbot graph that includes both a chatbot node 
        and a tool node. It defines tools, initializes the chatbot with tool 
        capabilities, and sets up conditional and direct edges between nodes. 
        The chatbot node is set as the entry point.
        """
        # creating tool node
        tools = get_tools()
        tool_node = create_tool_node(tools=tools)

        # Defining the nodes 
        self.chatbot_with_tools = ChatbotWithToolNodes(self.llm)
        self.graph_builder.add_node('Chatbot', self.chatbot_with_tools)
        self.graph_builder.add_node('Tools', tool_node)

        #defining the edges
        self.graph_builder.add_edge(START, 'Chatbot')
        self.graph_builder.add_conditional_edges('Chatbot', tools_condition)
        self.graph_builder.add_edge('tools','chatbot')

    def setup_graph(self, usecase:str):
        """
        Setsup the graph absed on the user input
        """
        if usecase=='Basic Chatbot':
            self.basic_chatbot_build_graph()
        elif usecase=='Chatbot with Tool':
            self.chatbot_with_tools_build_graph()
        else :
            self.ai_news_build_graph()
        return self.graph_builder.compile()
