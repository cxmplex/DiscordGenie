import asyncio

import discord

from modules.database.db import *


async def get_favorite_members(ctx):
    server = ctx.message.server
    ids = get_users_by_rank(3)
    members = list()
    for n in ids:
        members.append(server.get_member(n[0]))
    return members


async def mention_users(bot, users):
    to_mention = []
    for member in users:
        to_mention.append(member.mention)
    text = ' '.join(to_mention)
    await bot.say(text)


async def abuse_internal(bot, message, i: int = 1):
    if len(message.mentions) < 1:
        await bot.say("```\n"
                      "You didn't mention anyone.\nUsage:"
                      "\n.[c] [mentioned user] [number of iterations optional]\n```")
        return

    if i > 3:
        i = 3

    for member in message.mentions:
        prev_channel = member.voice.voice_channel
        for x in range(0, i):
            for channel in bot.get_all_channels():
                if channel.type == discord.ChannelType.voice:
                    await bot.move_member(member, channel)
                    await asyncio.sleep(.2)
            await asyncio.sleep(.2)
        # move the user back to the original channel
        await bot.move_member(member, prev_channel)


async def clear_internal(bot, channel, count):
    messages = []
    async for x in bot.logs_from(channel, limit=count):
        messages.append(x)
    await bot.delete_messages(messages)


async def get_record_holders(members):
    s_temp = [None, 0]
    s_t = [None, 0]
    s_c = [None, 0]
    for n, r, s, c, t in members:
        print(c)
        if s > s_temp[1]:
            s_temp[0] = n
            s_temp[1] = s
        if t > s_t[1]:
            s_t[0] = n
            s_t[1] = t
        if c > s_c[1]:
            s_c[0] = n
            s_c[1] = c
    return s_temp, s_t, s_c
