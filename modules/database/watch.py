
import re

from discord.ext import commands

from modules.cryptocurrency.crypto import get_coin_list
from modules.database.db import set_tasks


class Commands:
    def __init__(self, client):
        self.client = client
        self.coin_list = get_coin_list()

    @commands.command(pass_context=True)
    async def watch(self, ctx, service="", request=""):
        if ctx.message.channel.id != "424676030389944320":
            return
        if service != "crypto":
            await self.client.say("Invalid service!")
            return
        r = re.search("^(\w+)$", request)
        if not r:
            await self.client.say("Invalid request")
            return
        r = re.search("[A-Z]+", request)
        if r:
            request = self.coin_list['Data'][request]['CoinName']
        set_tasks(request)
        await self.client.say("```\nWatch request for Service: {} Request: {} added\n```".format(service, request))


def setup(client):
    client.add_cog(Commands(client))
