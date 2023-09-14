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
from sayvai_tools.tools.sql_database import Database
from sayvai_tools.tools.calendar import Calendar
from constants import prompt
from tools.vectorstore import vectordb 
from langchain.llms import OpenAI 
from langchain.chat_models import ChatOpenAI
from langchain.tools import HumanInputRun as human
from langchain.agents import AgentType, Tool, AgentExecutor , initialize_agent , OpenAIFunctionsAgent
from sqlalchemy import create_engine
from langchain.memory import ConversationSummaryBufferMemory
from tools.date import current_date


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
        self.memory = ConversationSummaryBufferMemory(llm=llm)
        self.tools = None
        self.human = None
        self.sql = None
        self.calendly = None
        self.system_message = prompt
        self.prompt = OpenAIFunctionsAgent.create_prompt(
            system_message=self.system_message,
        )
    
    
    def initialize_human(self) -> None:
        """Initialize the human"""
        self.human = human()
        return None
    
    

        
    def intialize_tools(self):
        """Initialize the tools"""
        if self.tools is None:
            self.tools = [
                Tool(
                    name="human",
                    func=self.human,
                    description="The human tool is used to interact with the user."
                ),
                Tool(
                    name="sql",
                    func=Database(llm=llm, engine=create_engine("sqlite:///sayvai.db"))._run,
                    description="useful to interaact with database (takes natural language input). contains details of all the employees from sayvai(table name: users). you can retrive details like email/mobile/designation"
                ),
                Tool(
                    name="pinecone",
                    func=vectordb,
                    description="useful when you need something about sayvai"
                ),
                Tool(
                    name="calendly",
                    func=Calendar()._run,
                    description="useful when you need to schedule an event. Input should be start and end time(Example input:2023,10,20,13,30/ 2023,10,20,14,00/mail"
                ),
                Tool(
                    name="datetime",
                    func=current_date,
                    description="useful when you need to know the current date and time"
                )
            ]
        else :
            print("Tools already initialized")
            

            
    def agent_inittialize(self, verbose: bool = False) -> None:
        """Initialize the agent"""
        # self.agent = initialize_agent(
        #     agent_type=AgentType.OPENAI_FUNCTIONS,
        #     llm=llm,
        #     tools=self.tools,
        #     verbose=verbose,
        # )
        self.agent = OpenAIFunctionsAgent(
            llm=llm,
            tools=self.tools,
            prompt=self.prompt,
        )
        agent_executor =AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=verbose,
            memory=self.memory,
        )
        return agent_executor
        
        
     
    def initialize(self, verbose: bool=False) -> None:
        """Initialize the assistant"""
        # self.initialize_vectordb()
        self.initialize_human()
        self.intialize_tools()
        self.agent_executor = self.agent_inittialize(verbose=verbose)
        return None
    
    def get_answer(self) -> str:
        """Get the answer from the agent"""
        return self.agent_executor.run("""
                                       interact with the user until he opt to quit(use human tool).
                                       To know the current date and time use datetime tool. Dont make up a time to schedule a meeting.
                                       If  mail is not provided, then the event will be scheduled for the user by accessiing the sql database for mail.
                                       """)
    
    
        