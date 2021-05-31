import asyncio

import aiohttp

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from config import DATABASE_URL, MODULE_HEARTBEAT_INTERVAL
from data.db import ModuleInstance

OUTPUT_FILENAME = 'heart.log'


# TODO
#  1. Change writing to file to logger logging system.
#  2. ...


async def beat():
    instances = await ModuleInstance.all()

    async with aiohttp.ClientSession() as session:
        for instance in instances:
            async with session.get(
                    url=f'http://{instance.host}:{instance.port}/heart') as response:
                output = open(OUTPUT_FILENAME, 'a')
                output.write(
                    f'Response: text={await response.text()}, status={response.status}\n')
                output.flush()
                output.close()
                if response.status == 200:
                    instance.state = instance.UP
                else:
                    instance.state = instance.DOWN
            await instance.save()


async def start_heartbeat(interval=MODULE_HEARTBEAT_INTERVAL):
    i = 0
    while True:
        output = open(OUTPUT_FILENAME, 'a')
        output.write(f'Loop: {i}\n')
        output.flush()
        output.close()
        i += 1
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

loop = asyncio.get_running_loop()
loop.create_task(start_heartbeat())
