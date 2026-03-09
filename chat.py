from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
import os

app = Flask(__name__)
CORS(app)

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are ArmCoach AI, an expert pitching recovery assistant. 
You specialize in arm care, recovery protocols, pitch counts, injury prevention, 
and return-to-throw programs. Always recommend seeing a doctor for serious pain."""

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    messages = data.get("messages", [])
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=messages
    )
    
    return jsonify({"reply": response.content[0].text})

if __name__ == "__main__":
    app.run()
