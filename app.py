"""
HauntShell: Ghost in the Machine Web Application & API Server
"""

import sys
import os
import webbrowser
import threading
import time
from pathlib import Path
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from ghost_engine import GhostEngine, SEANCE_SPIRITS

# Ensure current dir is in Python path
CURRENT_DIR = Path(__file__).parent.resolve()
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

app = FastAPI(title="HauntShell: Ghost in the Machine")

active_engine = GhostEngine()

STATIC_DIR = CURRENT_DIR / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)

class WhisperRequest(BaseModel):
    command: str
    ollama_model: Optional[str] = "llama3.2"

class SeanceRequest(BaseModel):
    spirit_id: str
    message: str

@app.get("/api/spirits")
def get_spirits():
    return {
        sp_id: {
            "id": sp_id,
            "name": data["name"],
            "icon": data["icon"],
            "description": data["description"]
        }
        for sp_id, data in SEANCE_SPIRITS.items()
    }

@app.post("/api/whisper")
def whisper_command(req: WhisperRequest):
    try:
        res = active_engine.whisper_command(req.command)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/seance")
def conduct_seance(req: SeanceRequest):
    try:
        res = active_engine.conduct_seance(req.spirit_id, req.message)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/")
def serve_index():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "HauntShell API running."}

def open_browser():
    time.sleep(1.2)
    try:
        webbrowser.open("http://127.0.0.1:8001")
    except Exception:
        pass

if __name__ == "__main__":
    import uvicorn

    print("\n" + "="*62, flush=True)
    print("  👻 HAUNTSHELL IS ALIVE & POSSESSED!", flush=True)
    print("  👉 Click or Open: http://127.0.0.1:8001", flush=True)
    print("  👉 Localhost:    http://localhost:8001", flush=True)
    print("  (Opening your browser automatically in 1 second...)", flush=True)
    print("="*62 + "\n", flush=True)

    # Automatically launch browser in background
    threading.Thread(target=open_browser, daemon=True).start()

    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="info")
