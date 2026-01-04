import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Initialize Groq Client
# Using the key provided by the user if not in env, but preferred from env/file
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable not set")

client = Groq(api_key=GROQ_API_KEY)

class GenerateRequest(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_response(request: GenerateRequest):
    try:
        print(f"Received prompt: {request.prompt}")
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are Jarves, a helpful and intelligent voice assistant. Keep your responses concise and conversational, suitable for a voice interface."
                },
                {
                    "role": "user",
                    "content": request.prompt,
                }
            ],
            model="llama-3.3-70b-versatile", # Updated to currently supported model
        )
        
        response_text = chat_completion.choices[0].message.content
        print(f"Generated response: {response_text}")
        return {"response": response_text}

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
