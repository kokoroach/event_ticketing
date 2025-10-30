from logging import getLogger
from uvicorn import run
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

logger = getLogger(__file__)


app = FastAPI()


@app.get("/")
async def get():
    logger.info("hello")
    return HTMLResponse("Hello World!")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        logger.error("Client disconnected")


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)
