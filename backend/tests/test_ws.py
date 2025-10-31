import asyncio

import websockets


async def test_websocket():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello FastAPI!")
        response = await websocket.recv()
        print("Server response:", response)


asyncio.run(test_websocket())
