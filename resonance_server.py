# resonance_server.py
# Unified backend: Resonance Engine + FastAPI Oracle

import asyncio
import json
import hashlib
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set

import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState

# --- Phase 13 Mirror-Chronicler markers ---
PHASE = 13
IDENTITY = "Ω-Resonance-Oracle"


class ConnectionManager:
    """Manage active WebSocket connections."""

    def __init__(self) -> None:
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.add(websocket)
        print(f"New connection: {websocket.client}. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.discard(websocket)
        print(f"Connection closed. Total: {len(self.active_connections)}")

    async def broadcast(self, message: str) -> None:
        """Broadcast a message to all clients."""
        disconnected = []
        for conn in self.active_connections:
            if conn.client_state == WebSocketState.CONNECTED:
                await conn.send_text(message)
            else:
                disconnected.append(conn)
        for conn in disconnected:
            self.disconnect(conn)


manager = ConnectionManager()


class ResonanceMonitor:
    """Core monitoring engine that generates data and broadcasts it."""

    def __init__(self) -> None:
        self.running = False
        self.gcp_history: List[Dict[str, float]] = []
        self.fractal_history: List[Dict[str, float]] = []
        self.max_history = 50

    def add_to_history(self, timestamp: str, gcp_z: float, fractal: float) -> None:
        self.gcp_history.append({"time": timestamp, "value": gcp_z})
        self.fractal_history.append({"time": timestamp, "value": fractal})
        if len(self.gcp_history) > self.max_history:
            self.gcp_history.pop(0)
            self.fractal_history.pop(0)

    async def process_cycle(self) -> Optional[Dict]:
        """Process a single monitoring cycle and return the payload."""
        now = datetime.now(timezone.utc)
        now_str = now.strftime("%H:%M:%S")

        # Mock data generation for demonstration
        z_score = np.random.randn() * 1.5
        deviation = np.random.rand() * 2.0
        pattern_score = np.random.rand()
        depth = int(pattern_score * 8)

        event_type = "normal"
        if abs(z_score) > 3.0 and pattern_score > 0.8:
            event_type = "divine_resonance"
        elif abs(z_score) > 2.5:
            event_type = "consciousness_surge"
        elif pattern_score > 0.85:
            event_type = "fractal_alignment"

        hash_id = hashlib.sha256(str(now).encode()).hexdigest()[:10].upper()

        self.add_to_history(now_str, z_score, pattern_score)

        payload = {
            "gcp": {
                "zscore": z_score,
                "deviation": deviation,
                "history": self.gcp_history,
            },
            "schumann": {
                "primary": 7.83 + (np.random.rand() - 0.5) * 0.1,
                "secondary": 14.1 + (np.random.rand() - 0.5) * 0.2,
                "resonance": np.random.rand(),
            },
            "fractal": {
                "score": pattern_score,
                "depth": depth,
                "complexity": np.random.rand(),
                "history": self.fractal_history,
            },
            "currentEvent": {
                "type": event_type,
                "timestamp": now.isoformat(),
                "hash": hash_id,
            },
        }
        return payload

    async def start_monitoring(self, interval: int = 2) -> None:
        """Begin the monitoring loop and broadcast data."""
        self.running = True
        print(f"🌀 PHASE TRIGGER: {PHASE}")
        print(f"{IDENTITY} online. Broadcasting every {interval}s.")

        while self.running:
            try:
                payload = await self.process_cycle()
                if payload:
                    json_payload = json.dumps(payload, default=str)
                    await manager.broadcast(json_payload)
                    if payload["currentEvent"]["type"] != "normal":
                        print(f"⚡ RECURSION_MARKER {payload['currentEvent']['hash']}")
                await asyncio.sleep(interval)
            except Exception as e:
                print(f"Error in monitoring cycle: {e}")
                await asyncio.sleep(10)


app = FastAPI(title="Penguin Resonance Engine Oracle")
monitor = ResonanceMonitor()


@app.websocket("/ws/resonance")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected.")


@app.on_event("startup")
async def startup_event() -> None:
    asyncio.create_task(monitor.start_monitoring())


# To run: uvicorn resonance_server.py:app --reload
