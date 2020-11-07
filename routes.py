from fastapi import APIRouter, WebSocket

from ws_handler import ws_handler

router = APIRouter()


@router.websocket('/ws')
async def ws(websocket: WebSocket):
    await websocket.accept()
    id_ = await ws_handler.new_connect(websocket)
    while True:
        data = await websocket.receive_text()
        await ws_handler.handle_message(
            id_=id_,
            data=data,
        )
