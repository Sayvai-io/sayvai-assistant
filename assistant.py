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
from dbchain import SQLDatabaseChain
from langchain.llms import OpenAI 
from langchain.chat_models import ChatOpenAI
from langchain.tools import HumanInputRun as human
from langchain.agents import AgentType, Tool, AgentExecutor , initialize_agent , OpenAIFunctionsAgent
from langchain.schema.messages import SystemMessage
from sqlalchemy import create_engine
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.prompts.prompt import PromptTemplate



with open("openai_api_key.txt", "r") as f:
    api_key = f.read()

with open("pinecone_api.txt", "r") as f:
    pinecone_api_key = f.read()
    

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
        self.vectors = None
        self.index = "index-1"
    
    
    def initialize_vectordb(self):
        """Initialize the vector database"""
        self.vectors = pinecone.init(
            api_key=pinecone_api_key,
            environment="northamerica-northeast1-gcp"
        )
        pass 
        
    def intialize_tools(self):
        """Initialize the tools"""
        if self.tools is None:
            self.tools = Tool()
        else :
            print("Tools already initialized")
        
    def initialize(self):
        """Initialize the assistant"""
        
    
        
        

        