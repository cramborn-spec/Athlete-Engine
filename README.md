# Athlete Engine

A performance tracking platform built for baseball pitchers. Athletes and coaches 
can log daily recovery metrics, throwing workload, and pitch data — and receive 
AI-powered coaching analysis in real time.

## Features

- **Daily Athlete Survey** — Log sleep, energy, focus, soreness, and stress on a 1-5 scale
- **Trackman Integration** — Upload pitch PDFs to visualize velocity, spin rate, and movement data
- **AI Analysis** — Ask performance questions and receive dual AI responses from Gemini and Groq
- **Coach Portal** — Staff can input workload, throwing volume, and lifting blocks per athlete
- **Performance Scoring** — Eleanor's Readiness Score calculates a daily 1-5 readiness rating

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React + TypeScript (Google AI Studio) |
| Backend | FastAPI (Python), deployed on Render |
| Database | Google Sheet |
| AI — Performance | Google Gemini |
| AI — Pitching Coach | Groq (LLaMA 3.3 70B) |

## Backend API

Live at: `https://pitchiq-backend.onrender.com`

Interactive docs: `https://pitchiq-backend.onrender.com/docs`

## Backend Setup

1. Clone this repo
2. Install dependencies:
```
   pip install -r requirements.txt
```
3. Add your Groq API key as an environment variable:
```
   GROQ_API_KEY=your_key_here
```
4. Run locally:
```
   uvicorn main:app --reload
```
