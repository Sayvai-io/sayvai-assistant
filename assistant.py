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
import pinecone
from dbbase import SQLDatabase
from vectorstore import vectordb
from dbchain import SQLDatabaseChain 
from langchain.llms import OpenAI 
from langchain.chat_models import ChatOpenAI
from langchain.tools import HumanInputRun as human
from langchain.agents import AgentType, Tool, AgentExecutor , initialize_agent , OpenAIFunctionsAgent
from langchain.schema.messages import SystemMessage
from sqlalchemy import create_engine
from langchain.prompts.prompt import PromptTemplate



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
        self.memory = None
        self.tools = None
        self.human = None
        self.sql = None
        self.calendly = None
        self.system_message = SystemMessage(content="You are assistant that works for sayvai.Interacrt with user untill he opt to exit")
        self.prompt = OpenAIFunctionsAgent.create_prompt(
            system_message=self.system_message,
        )
    
    
    def initialize_human(self) -> None:
        """Initialize the human"""
        self.human = human()
        return None
    
    def initialize_sql(self) -> None:
        """Initialize the sql database"""
        self.sql = create_engine(
            "sqlite:///sayvai.db",
            echo=True,
            future=True,
        )
        return None
    
    
    def sql_chain(self):
        """Initialize the sql database chain"""
        db = SQLDatabase(engine = self.sql)
        sql_db_chain = SQLDatabaseChain.from_llm(
        llm=llm,
        db=db,
        )
        return sql_db_chain
        
        
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
                    func=self.sql_chain.run,
                    description="useful to fetch database (takes natural language input)."
                ),
                Tool(
                    name="pinecone",
                    func=vectordb,
                    description="useful when you need something about sayvai"
                ),
            ]
        else :
            print("Tools already initialized")
            

            
    def initialize_agent(self, verbose: bool = False) -> None:
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
        )
        return agent_executor
        
        
     
    def initialize(self) -> None:
        """Initialize the assistant"""
        # self.initialize_vectordb()
        self.initialize_human()
        self.initialize_sql()
        self.intialize_tools()
        self.initialize_agent(verbose=True)
        return None
    
    def get_answer(self, question: str) -> str:
        """Get the answer from the agent"""
        agent_executor = self.initialize_agent()
        return agent_executor.run(question)
    
        
    
        
    
        
        

        