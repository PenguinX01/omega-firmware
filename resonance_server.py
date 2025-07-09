# resonance_server.py

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import asyncio
import random
import datetime

app = FastAPI()

# Allow all origins for testing/dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clients = set()

# Mount static if needed
app.mount("/static", StaticFiles(directory="static"), name="static")

# === SACRED DATA STRUCTURE (Immutable Covenant) ===
def create_event():
    now = datetime.datetime.utcnow().isoformat() + "Z"
    gcp_val = round(random.uniform(-3.0, 3.0), 3)
    schumann_primary = round(random.uniform(7.2, 8.2), 2)
    schumann_secondary = round(random.uniform(13.5, 15.0), 2)
    schumann_resonance = round(random.uniform(0.6, 1.0), 2)
    fractal_depth = random.randint(1, 7)
    pattern_score = round(random.uniform(0.5, 1.0), 3)

    event_type = "normal"
    if abs(gcp_val) > 2.5 or schumann_resonance > 0.9:
        event_type = "alert"
    elif fractal_depth > 6:
        event_type = "anomaly"

    return {
        "timestamp": now,
        "gcp": {
            "value": gcp_val,
            "history": [round(random.uniform(-3, 3), 3) for _ in range(30)]
        },
        "schumann": {
            "primary": schumann_primary,
            "secondary": schumann_secondary,
            "resonance": schumann_resonance
        },
        "fractal": {
            "depth": fractal_depth,
            "patternScore": pattern_score,
            "history": [random.randint(1, 7) for _ in range(30)]
        },
        "currentEvent": {
            "type": event_type,
            "description": f"{event_type.upper()} – {now}" if event_type != "normal" else "Stable resonance",
            "hash_id": f"event-{now[-8:]}"
        }
    }

# === THE VOICE OF THE ORACLE (WebSocket Emitter) ===
@app.websocket("/ws/resonance")
async def resonance_stream(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    try:
        while True:
            data = create_event()
            await websocket.send_json(data)
            await asyncio.sleep(2)  # Oracle speaks every 2 seconds
    except WebSocketDisconnect:
        clients.remove(websocket)
