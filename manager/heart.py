import asyncio

import aiohttp

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from config import DATABASE_URL, MODULE_HEARTBEAT_INTERVAL
from data.db import ModuleInstance


async def beat():
    instances = await ModuleInstance.all()

    async with aiohttp.ClientSession() as session:
        for instance in instances:
            async with session.get(
                    url=f'http://{instance.host}:{instance.port}') as response:
                if response.status == 200:
                    instance.state = instance.UP
                else:
                    instance.state = instance.DOWN
            await instance.save()


async def start_heartbeat(interval=MODULE_HEARTBEAT_INTERVAL):
    while True:
        await asyncio.sleep(interval)
        await beat()


app = FastAPI()

register_tortoise(
    app=app,
    db_url=DATABASE_URL,
    modules={'manager': ["data.db.models"]},
    generate_schemas=False,
    add_exception_handlers=True
)

# asyncio.run(start_heartbeat())
