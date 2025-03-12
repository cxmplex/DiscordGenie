
import asyncio

import discord

from modules.cryptocurrency.crypto import get_info, get_message
from modules.database.db import get_tasks
from modules.moderation.moderation import clear_internal

messages = {}


async def run_tasks(client):
    await client.wait_until_ready()
    channel = discord.Object(id='422504096990494741')
    await clear_internal(client, channel, 10)
    while not client.is_closed:
        tasks = get_tasks()
        for service, request in tasks:
            info = get_info(request)
            text = get_message(info)
            if request in messages:
                message = messages[request]
                await client.edit_message(message, text)
                continue
            message = await client.send_message(channel, text)
            messages[request] = message
        await asyncio.sleep(120)
