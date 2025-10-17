from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import os

# Load .env file (for API key)
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Request model for symptoms
class SymptomRequest(BaseModel):
    symptoms: str

# Serve the HTML page
@app.get("/")
def serve_home():
    return FileResponse("index.html")

# Main endpoint for symptom checking
@app.post("/check_symptoms")
async def check_symptoms(request: SymptomRequest):
    messages = [
        {"role": "system", "content": "You are a healthcare assistant."},
        {"role": "user", "content": f"Symptoms: {request.symptoms}"}
    ]
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
        )
        return {"result": response.choices[0].message.content.strip()}
    except Exception as e:
        return {"result": f"Error: {type(e).__name__} - {str(e)}"}
