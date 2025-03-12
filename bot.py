
import time

import discord
from discord.ext import commands

from config.build_config import read_api_key
from modules.database.db import *
from modules.database.task_runner import run_tasks

user_voice = {}
client = commands.Bot(command_prefix='.')
extensions = ["modules.moderation.moderation",
              "modules.games.games",
              "modules.dotabuff.dotabuff",
              "modules.cryptocurrency.crypto",
              "modules.database.watch",
              "modules.audio.audio",
              "modules.combile_bot.compile"
              ]


@client.event
async def on_ready():
    print("Client has been loaded! :)")
    await client.change_presence(game=discord.Game(name="Ready for commands!"), afk=False)


@client.event
async def on_message(message):
    set_user_count(message.author.id)
    await client.process_commands(message)


@client.event
async def on_voice_state_update(before, after):
    # joined a channel
    if before.voice_channel is None or before.voice_channel.id == '422504523014209565':
        entry_time = int(time.time())
        user_voice[before.id] = entry_time
        print(before.name + " joined channel")
    # left a channel
    elif after.voice_channel is None or after.voice_channel.id == '422504523014209565':
        total_time = 0
        try:
            total_time = int(time.time()) - user_voice[after.id]
        except:
            return
        if total_time >= 43200:
            print("Something is clearly wrong, ignoring")
            user_voice[after.id] = 0
            return
        set_user_time(total_time, after.id)
        user_voice[after.id] = 0
        print(before.name + " left channel after {} seconds".format(total_time))

if __name__ == "__main__":
    for extension in extensions:
        try:
            client.load_extension(extension)
            print('Loaded extension {}'.format(extension))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    client.loop.create_task(run_tasks(client))
    client.run(read_api_key())
