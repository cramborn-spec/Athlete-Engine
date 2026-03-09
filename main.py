from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
from database import init_db, get_db

app = FastAPI(title="PitchIQ Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class PitchSession(BaseModel):
    pitcher_name: str
    pitch_type: str
    velocity: float
    spin_rate: int
    result: str

class AnalyzeRequest(BaseModel):
    pitcher_name: str
    pitch_type: str
    velocity: float
    spin_rate: int
    result: str

@app.get("/")
def root():
    return {"message": "PitchIQ API is running!"}

@app.post("/pitchers")
def save_pitch(session: PitchSession):
    conn = get_db()
    conn.execute(
        "INSERT INTO pitch_sessions (pitcher_name, pitch_type, velocity, spin_rate, result) VALUES (?, ?, ?, ?, ?)",
        (session.pitcher_name, session.pitch_type, session.velocity, session.spin_rate, session.result)
    )
    conn.commit()
    conn.close()
    return {"message": "Pitch saved successfully"}

@app.get("/pitchers/{pitcher_name}")
def get_pitcher_history(pitcher_name: str):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM pitch_sessions WHERE pitcher_name = ? ORDER BY created_at DESC",
        (pitcher_name,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.post("/analyze")
async def analyze_pitcher(data: AnalyzeRequest):
    prompt = f"""
    You are an expert baseball pitching coach. Analyze this pitch data and give short, actionable feedback:

    Pitcher: {data.pitcher_name}
    Pitch Type: {data.pitch_type}
    Velocity: {data.velocity} mph
    Spin Rate: {data.spin_rate} rpm
    Result: {data.result}

    Give 2-3 sentences of coaching advice based on these numbers.
    """

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={
                "model": "llama3-8b-8192",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 200
            }
        )

   result = response.json()
    
    # Show the full Groq response if something goes wrong
    if "choices" not in result:
        return {"error": "Groq API error", "details": result}
    
    analysis = result["choices"][0]["message"]["content"]
    return {"analysis": analysis}
