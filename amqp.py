from asyncio import get_event_loop

import aio_pika

from ws_handler import ws_handler


class AMQPHandler:
    QUEUE_NAME = 'test_queue'

    def __init__(self):
        self.connection = None
        self.channel = None

    async def init(self):
        self.connection = await aio_pika.connect_robust(
            "amqp://guest:guest@127.0.0.1:5672/", loop=get_event_loop()
        )
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=100)
        exchange = await self.channel.declare_exchange(
            self.QUEUE_NAME,
            aio_pika.ExchangeType.FANOUT,
        )
        queue = await self.channel.declare_queue(exclusive=True)
        await queue.bind(exchange)
        await queue.consume(self.handle_message)
        return self.connection

    @classmethod
    async def handle_message(cls, message: aio_pika.IncomingMessage):
        async with message.process():
            await ws_handler.notify_all(
                message=message.body,
            )

    async def publish(self, message_text: str):
        message = aio_pika.Message(
            body=message_text.encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )
        exchange = await self.channel.declare_exchange(
            self.QUEUE_NAME,
            aio_pika.ExchangeType.FANOUT,
        )
        await exchange.publish(
            message,
            routing_key=self.QUEUE_NAME,
        )


amqp_handler = AMQPHandler()
