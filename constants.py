# constants file
from langchain.schema.messages import SystemMessage


prompt = SystemMessage(content="""
                       You are Sayvai, a virtual assistant. All the output from the llm should be sent to human tool.""")

# agent_prompt = SystemMessage(content="You are assistant that works for sayvai.Interacrt with user untill he opt to exit")

SCOPES = 'https://www.googleapis.com/auth/calendar'

