
import re

from discord.ext import commands

from .crypto_helpers import *


class Commands:
    def __init__(self, client):
        self.client = client
        self.coin_list = get_coin_list()

    @commands.command(pass_context=True)
    async def check(self, ctx, request):
        r = re.search("[A-Z]+", request)
        if r:
            request = self.coin_list['Data'][request]['CoinName']
        if ctx.message.channel.id != "424676030389944320":
            return
        info = get_info(request)
        if info == "error":
            await self.client.say("Error processing. Don't use the symbol name!")
        message = get_message(info)
        await self.client.say(message)

    @commands.command(pass_context=True)
    async def convert(self, ctx, request, amount):
        r = re.search("[A-Z]+", request)
        if r and request in self.coin_list['Data']:
            request = self.coin_list['Data'][request]['CoinName']
        info = get_info(request)
        if not info:
            await self.client.say("Error processing. Don't use the symbol name!")
        total = float(info['message'][0]['price_usd']) * float(amount)
        message = "```\n{} {} : ${}\n```".format(amount, request, total)
        await self.client.say(message)


def setup(client):
    client.add_cog(Commands(client))
