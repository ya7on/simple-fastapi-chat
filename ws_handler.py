from typing import Dict
from uuid import uuid4

from fastapi import WebSocket


class WSHandler:
    def __init__(self):
        self.connection: Dict[uuid4, WebSocket] = {}

    async def new_connect(self, websocket: WebSocket) -> uuid4:
        id_ = uuid4()

        self.connection[id_] = websocket
        await websocket.send_text('Welcome')  # TODO
        return id_

    async def handle_message(self, *, id_, data):
        from amqp import amqp_handler

        ws_inst = self.connection[id_]
        await ws_inst.send_text(f'Recieved {data}')
        await amqp_handler.publish(data)

    async def notify_all(self, *, message):
        for id_, ws_inst in self.connection.items():
            await ws_inst.send_text(f'New message {message}')


ws_handler = WSHandler()
