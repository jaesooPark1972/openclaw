from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
import uvicorn
from openai import OpenAI
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv(r"D:/OpenClaw/.env")

app = FastAPI(title="Pony Alpha API Server")

class PonyChatRequest(BaseModel):
    user_prompt: str
    system_prompt: Optional[str] = "You are Pony Alpha, a helpful AI assistant."
    max_tokens: Optional[int] = 4096
    temperature: Optional[float] = 0.7

@app.post("/api/chat/pony")
async def chat_pony(req: PonyChatRequest):
    """
    [Pony Alpha API] Direct Interface to OpenRouter Pony Alpha Model.
    """
    or_key = os.getenv("OPENROUTER_API_KEY")
    if not or_key: or_key = os.getenv("OPENAI_API_KEY") 
    
    if not or_key:
        raise HTTPException(status_code=500, detail="OPENROUTER_API_KEY not found in environment")
        
    try:
        # Direct OpenRouter client
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=or_key,
        )
        
        start_t = time.time()
        completion = client.chat.completions.create(
            model="openrouter/pony-alpha",
            messages=[
                {"role": "system", "content": req.system_prompt},
                {"role": "user", "content": req.user_prompt},
            ],
            max_tokens=req.max_tokens,
            temperature=req.temperature,
        )
        duration = time.time() - start_t
        reply = completion.choices[0].message.content
        
        return {
            "model": "openrouter/pony-alpha",
            "content": reply, 
            "usage": completion.usage.model_dump() if completion.usage else {},
            "latency": duration
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8090)
