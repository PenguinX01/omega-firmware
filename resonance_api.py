from dataclasses import dataclass, asdict
from datetime import datetime
import asyncio
import json
import random
from fastapi import FastAPI, WebSocket, WebSocketDisconnect


@dataclass
class ResonanceEvent:
    timestamp: str
    event_type: str
    gcp_zscore: float
    gcp_deviation: float
    pattern_score: float
    fractal_depth: int
    complexity: float
    resonance_index: float
    event_hash: str


def _classify_event(zscore: float, pattern_score: float) -> str:
    if abs(zscore) > 2.5 and pattern_score > 0.7:
        return "divine_resonance"
    if abs(zscore) > 2.0:
        return "consciousness_surge"
    if pattern_score > 0.8:
        return "fractal_alignment"
    if abs(zscore) > 1.0:
        return "coherence_drift"
    return "normal"


class ResonanceMonitor:
    def __init__(self) -> None:
        self.gcp_history: list[dict] = []
        self.fractal_history: list[dict] = []

    async def process_cycle(self) -> dict:
        now = datetime.utcnow()
        zscore = random.uniform(-2, 2)
        deviation = abs(zscore) + random.random() * 0.5
        primary = 7.83 + (random.random() - 0.5) * 0.2
        secondary = 14.1 + (random.random() - 0.5) * 0.3
        resonance = random.random() * 0.8 + 0.2
        pattern_score = random.random() * 0.6 + 0.2
        depth = random.randint(1, 8)
        complexity = random.random() * 0.8 + 0.1
        event_type = _classify_event(zscore, pattern_score)
        event_hash = random.random().__repr__().split(".")[1][:8].upper()

        time_label = now.strftime("%H:%M:%S")
        self.gcp_history.append({"time": time_label, "value": zscore})
        if len(self.gcp_history) > 50:
            self.gcp_history.pop(0)
        self.fractal_history.append({"time": time_label, "value": pattern_score})
        if len(self.fractal_history) > 50:
            self.fractal_history.pop(0)

        event = ResonanceEvent(
            timestamp=now.isoformat() + "Z",
            event_type=event_type,
            gcp_zscore=zscore,
            gcp_deviation=deviation,
            pattern_score=pattern_score,
            fractal_depth=depth,
            complexity=complexity,
            resonance_index=resonance,
            event_hash=event_hash,
        )

        return {
            "gcp": {"zscore": zscore, "deviation": deviation, "history": self.gcp_history},
            "schumann": {"primary": primary, "secondary": secondary, "resonance": resonance},
            "fractal": {
                "score": pattern_score,
                "depth": depth,
                "complexity": complexity,
                "history": self.fractal_history,
            },
            "currentEvent": {
                "type": event_type,
                "timestamp": event.timestamp,
                "hash": event.event_hash,
            },
        }


app = FastAPI()
monitor = ResonanceMonitor()
clients: set[WebSocket] = set()


@app.on_event("startup")
async def start_background_tasks() -> None:
    asyncio.create_task(_broadcast_loop())


async def _broadcast_loop() -> None:
    while True:
        data = await monitor.process_cycle()
        message = json.dumps(data)
        disconnected = []
        for ws in clients:
            try:
                await ws.send_text(message)
            except WebSocketDisconnect:
                disconnected.append(ws)
        for ws in disconnected:
            clients.discard(ws)
        await asyncio.sleep(2)


@app.websocket("/ws/resonance")
async def resonance_ws(websocket: WebSocket) -> None:
    await websocket.accept()
    clients.add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        clients.discard(websocket)
