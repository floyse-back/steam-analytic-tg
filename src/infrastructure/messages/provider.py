import asyncio
import json

from aio_pika import connect,Message

from src.shared.config import RABBITMQ_CONNECTION


class EventProvider:
    def __init__(self):
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await connect(RABBITMQ_CONNECTION)
        self.channel = await self.connection.channel()

    async def send_message(self,data:dict,queue:str)->None:
        self.connection = await connect(RABBITMQ_CONNECTION)
        self.channel = await self.connection.channel()

        await self.channel.declare_queue(queue, durable=True)
        message = Message(json.dumps(data).encode())
        await self.channel.default_exchange.publish(message, routing_key=f'{queue}')
        await self.connection.close()