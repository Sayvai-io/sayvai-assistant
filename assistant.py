# langchain code for the assistant
"""
1) Tools
 1.1) Pinecone
 1.2) human
 1.3) Sql
 1.4) calendly
2) Agent
3) Memory 
 3.1) summarization
"""
import os

from langchain.agents import AgentExecutor, OpenAIFunctionsAgent, Tool
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryMemory
from langchain.schema.messages import SystemMessage
from langchain.tools import HumanInputRun as human

# from tools.constants import agent_prompt
from tools.database import DatabaseChain
from tools.vectorstore import vectordb
from tools.cal_event import event

with open("openai_api_key.txt", "r") as f:
    api_key = f.read()
    
os.environ["OPENAI_API_KEY"] = api_key

llm = ChatOpenAI(
    temperature=0.4,
)

class Assistant:
    """
    The assistant is a class that is used to interact with the user and the agent. 
    It is the main interface for the user to interact with the agent."""
    def __init__(self):
        self.agent = None
        self.tools = None
        self.agent_executor = None
        self.prompt = None
        self.memory = ConversationSummaryMemory(llm=llm, memory_key='history')
        
    def intialize_tools(self):
        """Initialize the tools"""
        if self.tools is None:
            self.tools = [
                Tool(
                    name="human",
                    func=human,
                    description="The human tool is used to interact with the user."
                ),
                Tool(
                    name="sql",
                    func=DatabaseChain,
                    description="useful to fetch database (takes natural language input)."
                ),
                Tool(
                    name="pinecone",
                    func=vectordb,
                    description="useful when you need something about sayvai"
                ),
                Tool(
                    name="calendar",
                    func=event,
                    description="useful when you need to schedule an event. Input should be start and end time(Example input:2023,10,20,13,30/ 2023,10,20,14,00)."
                )
            ]
        else :
            print("Tools already initialized")
             
    def initialize_agent(self, verbose: bool = False) -> None:
        """Initialize the agent"""
        self.prompt = OpenAIFunctionsAgent.create_prompt(system_message=SystemMessage(content="You are assistant that works for sayvai.Interacrt with user untill he opt to exit. Use human tool to interact with the user"))
        self.agent = OpenAIFunctionsAgent(
            llm=llm,
            tools=self.tools,
            prompt=self.prompt
            )
        agent_executor =AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=verbose,
            memory=self.memory
        )
        return agent_executor
            
    def initialize(self) -> None:
        """Initialize the assistant"""
        self.intialize_tools()
        self.agent_executor=self.initialize_agent(verbose=True)
        return None
    
    def get_answer(self, question: str) -> str:
        """Get the answer from the agent"""
        return self.agent_executor.run(question)
