from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


from fastapi import FastAPI
from pydantic import BaseModel
from orchestrator import Orchestrator  # Import your Orchestrator class

# Initialize FastAPI app
app = FastAPI()

# Initialize Orchestrator
orchestrator = Orchestrator()

# Define request model
class UserInputRequest(BaseModel):
    user_input: str  # Input text from the user

# Define response model (optional)
class OrchestratorResponse(BaseModel):
    response: str  # The response from orchestrator.start()

# API endpoint to handle user input
@app.post("/api", response_model=OrchestratorResponse)
async def process_input(request: UserInputRequest):
    """
    Receives a user input, sends it to orchestrator.start(), 
    and returns the response.
    """
    print(request.user_input)
    response = orchestrator.start(request.user_input)  # Call orchestrator
    return {"response": str(response)}

# Root endpoint (optional)
@app.get("/")
async def root():
    return {"message": "FastAPI LangGraph Orchestrator is running!"}
