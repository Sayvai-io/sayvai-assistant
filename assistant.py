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
from langchain.chains import question_answering 
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
    
    
    def initialize_vectordb(self) -> None:
        """Initialize the vector database"""
        self.vectors = pinecone.init(
            api_key=pinecone_api_key,
            environment="northamerica-northeast1-gcp"
        )
        return None
    
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
                    func=self.sql_chain,
                    description="The sql tool is used to interact with the sql database."
                ),
                Tool(
                    name="pinecone",
                    func=self.vectors,
                    description="The pinecone tool is used to interact with the vector database."
                ),
            ]
        else :
            print("Tools already initialized")
            
    def sql_chain(self):
        """Initialize the sql database chain"""
        db = SQLDatabase(engine = self.sql)
        sql_db_chain = SQLDatabaseChain.from_llm(
            llm=llm,
            db=db,
        )
        return sql_db_chain.run()
    
    def get_similar(self, query):
        """Get similar query from the vector database"""
        # get existing index
        search = Pinecone.from_existing_index(
            index_name=self.index,
            embedding=OpenAIEmbeddings(),
            namespace="Proposal-investors"
        )
        similar_docs = search.similarity_search_with_score(query, k=2)
        # write a Q and A chain to get the answer
        qachain = question_answering.load_qa_chain(
            llm=llm,
            chain_type="stuff",
            
        )
        print(similar_docs[0][0].page_content)
        return qachain.run(input_documents=similar_docs[0][0], question=query)
        
     
    def initialize(self):
        """Initialize the assistant"""
        self.initialize_vectordb()
        self.initialize_human()
        self.initialize_sql()
        self.intialize_tools()
        
    
        
        

        