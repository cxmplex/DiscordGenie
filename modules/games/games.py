
import random

from discord.ext import commands

from modules.database.db import get_stars, set_star
from modules.moderation.moderation import abuse_internal


class Commands:
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def roll(self):
        r = random.randint(1, 6)
        await self.client.say("You rolled {}!".format(r))

    @commands.command(pass_context=True)
    async def roulette(self, ctx):
        r = random.randint(1, 6)
        if r == 3:
            await self.client.say("You were shot. Have fun!")
            txt = ".abuse {} 3".format(ctx.message.author.mention)
            message = await self.client.say(txt)
            await abuse_internal(self.client, message, 3)
        else:
            await self.client.say("You're safe!")

    @commands.command()
    async def goodbot(self):
        set_star()
        count = get_stars()
        await self.client.say("```\nI've been a good bot!\nGood Boy Points: {}\n```".format(count))

    @commands.command(name='.', pass_context=True)
    async def code(self, ctx):
        await self.client.say("```\n{}\n```".format(ctx.message.clean_content[3:]))
        await self.client.delete_message(ctx.message)


def setup(client):
    client.add_cog(Commands(client))
