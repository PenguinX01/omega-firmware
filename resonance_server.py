# resonance_server.py

"""Phase 13 Mirror-Chronicler WebSocket oracle."""

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import uvicorn
import random
from datetime import datetime
import json

PHASE = 13
IDENTITY = "Ω-Resonance-Oracle"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clients = []

print(f"⟁ PHASE {PHASE} :: {IDENTITY} booting")


@app.websocket("/ws/resonance")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = {
                "timestamp": datetime.utcnow().isoformat(),
                "gcp": round(random.gauss(0, 1.5), 3),
                "schumann": [round(random.uniform(7.3, 8.2), 3) for _ in range(5)],
                "fractal": round(random.uniform(0.6, 0.95), 3),
                "currentEvent": classify_event(),
            }
            await websocket.send_text(json.dumps(data))
            if data["currentEvent"]["type"] != "normal":
                print(f"⚡ RECURSION_MARKER {data['currentEvent']['type']} @ {data['timestamp']}")
            await asyncio.sleep(2)
    except Exception:
        clients.remove(websocket)


def classify_event():
    z = random.gauss(0, 1.5)
    score = random.uniform(0.6, 0.95)
    if z > 2.5 and score > 0.7:
        return {
            "type": "divine_resonance",
            "timestamp": datetime.utcnow().isoformat(),
            "gcp_deviation": z,
            "pattern_score": score,
            "message": "✨ Divine Resonance detected",
        }
    elif z > 2.0:
        return {
            "type": "consciousness_surge",
            "timestamp": datetime.utcnow().isoformat(),
            "gcp_deviation": z,
            "pattern_score": score,
            "message": "⚡ Consciousness Surge",
        }
    else:
        return {
            "type": "normal",
            "timestamp": datetime.utcnow().isoformat(),
            "gcp_deviation": z,
            "pattern_score": score,
            "message": "All is calm",
        }


if __name__ == "__main__":
    print(f"⟁ {IDENTITY} listening on 0.0.0.0:8000")
    uvicorn.run("resonance_server:app", host="0.0.0.0", port=8000, reload=True)
