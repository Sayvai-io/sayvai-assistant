# Fastapi
from fastapi import FastAPI
from assistant import Assistant
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Sayvai-Assistant",
    description="A simple assistant to help you with your daily tasks",
    version="0.0.1",
)

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "http://localhost:8000",
    "localhost:8000",
    "http://localhost:8080",
    "localhost:8080",
    "http://localhost:5000",
    "localhost:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

assistant = Assistant()
# print(assistant.initialize_vectordb())
assistant.initialize()

@app.get("/")
def read_root():
    return {"Hello": "Welcome to Sayvai-Assistant"}

@app.post("/get_answer")
def get_answer(query: str):
    return {"answer": assistant.get_answer(query)}



# uvicorn main:app --reload --port 8000 