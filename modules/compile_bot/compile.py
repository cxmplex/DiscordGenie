
from discord.ext import commands


class Commands:
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def compileme(self, ctx):
        await self.client.say("This feature is not available yet.")


def setup(client):
    client.add_cog(Commands(client))
