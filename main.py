import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import re

# Import Skills
try:
    from skills.web_search import WebSearchSkill
    from skills.app_control import AppControlSkill
    from skills.system_skills import SystemSkills
except ImportError:
    # Fallback if running from a different directory context, though typical uvicorn run should work
    from .skills.web_search import WebSearchSkill
    from .skills.app_control import AppControlSkill
    from .skills.system_skills import SystemSkills

# Load environment variables
load_dotenv()

app = FastAPI()

# Initialize Groq Client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable not set")

client = Groq(api_key=GROQ_API_KEY)

# Initialize Skills
web_search = WebSearchSkill()
app_control = AppControlSkill()

class GenerateRequest(BaseModel):
    prompt: str

# Initialize Memory
conversation_history = [
    {"role": "system", "content": "You are Jarves, a helpful and intelligent voice assistant. Keep your responses concise and conversational, suitable for a voice interface."}
]
MAX_HISTORY = 20

@app.post("/generate")
async def generate_response(request: GenerateRequest):
    global conversation_history
    try:
        prompt_lower = request.prompt.lower()
        print(f"Received prompt: {request.prompt}")

        # --- Skill Routing Logic (Keyword Matching) ---
        
        # 1. App Control
        # Open App
        if "open" in prompt_lower:
            words = prompt_lower.split()
            if "open" in words:
                idx = words.index("open")
                if idx + 1 < len(words):
                    potential_app = words[idx + 1]
                    # Handle "open the [app]"
                    if potential_app == "the" and idx + 2 < len(words):
                        potential_app = words[idx + 2]
                    app_name = potential_app
                    if app_name in app_control.app_map or "app" in prompt_lower or True: 
                        return {"response": app_control.open_app(app_name)}

        # Close App
        if "close" in prompt_lower:
             words = prompt_lower.split()
             if "close" in words:
                idx = words.index("close")
                if idx + 1 < len(words):
                    app_name = words[idx + 1]
                    return {"response": app_control.close_app(app_name)}

        # 2. Web Search
        if "search for" in prompt_lower or "google" in prompt_lower:
            query = prompt_lower.replace("search for", "").replace("google", "").strip()
            if query:
                return {"response": web_search.search(query)}

        # 3. System Control - Volume
        if "volume" in prompt_lower:
            if "mute" in prompt_lower or "unmute" in prompt_lower:
                return {"response": SystemSkills.mute_volume()}
            elif "set" in prompt_lower: 
                match = re.search(r'\d+', prompt_lower)
                if match:
                    level = int(match.group())
                    return {"response": SystemSkills.set_volume(level)}
            elif "up" in prompt_lower or "increase" in prompt_lower:
                return {"response": SystemSkills.set_volume(50)} 
            elif "down" in prompt_lower or "decrease" in prompt_lower:
                 return {"response": "Lowering volume..."} 

        # 4. System Control - Brightness
        if "brightness" in prompt_lower:
             match = re.search(r'\d+', prompt_lower)
             if match and "set" in prompt_lower:
                level = int(match.group())
                return {"response": SystemSkills.set_brightness(level)}

        # 5. Advanced System Control
        if "lock" in prompt_lower and ("pc" in prompt_lower or "computer" in prompt_lower):
            return {"response": SystemSkills.lock_pc()}
        
        if "screenshot" in prompt_lower:
            return {"response": SystemSkills.take_screenshot()}
        
        if "minimize" in prompt_lower:
            return {"response": SystemSkills.minimize_all()}
            
        if "type" in prompt_lower:
            text_to_type = prompt_lower.replace("type", "", 1).strip()
            if text_to_type:
                return {"response": SystemSkills.type_text(text_to_type)}
        
        if "shutdown" in prompt_lower:
             return {"response": SystemSkills.shutdown_pc()}

        # --- Memory Management & LLM Fallback ---
        
        # Add User Message to History
        conversation_history.append({"role": "user", "content": request.prompt})
        
        # Truncate History if too long (keep system prompt + last N messages)
        if len(conversation_history) > MAX_HISTORY:
            # Keep index 0 (System) and the last (MAX_HISTORY - 1) messages
            conversation_history = [conversation_history[0]] + conversation_history[-(MAX_HISTORY-1):]

        chat_completion = client.chat.completions.create(
            messages=conversation_history,
            model="llama-3.3-70b-versatile",
        )
        
        response_text = chat_completion.choices[0].message.content
        
        # Add Assistant Response to History
        conversation_history.append({"role": "assistant", "content": response_text})
        
        print(f"Generated response: {response_text}")
        return {"response": response_text}

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reset")
async def reset_memory():
    global conversation_history
    conversation_history = [
        {"role": "system", "content": "You are Jarves, a helpful and intelligent voice assistant. Keep your responses concise and conversational, suitable for a voice interface."}
    ]
    return {"message": "Memory reset."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
