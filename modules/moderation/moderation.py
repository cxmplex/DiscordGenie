
import datetime
import re

from modules.custom_checks.auth import *
from .mod_helpers import *


class Commands:
    def __init__(self, client):
        self.client = client

    @auth_check()
    @commands.command(pass_context=True)
    async def assemble(self, ctx):
        members = await get_favorite_members(ctx)
        if ctx.message.author in members:
            members.remove(ctx.message.author)
        await mention_users(self.client, members)

    @auth_check()
    @commands.command(pass_context=True)
    async def abuse(self, ctx, mention, i=1):
        await abuse_internal(self.client, ctx.message, i)

    @auth_check()
    @commands.command(pass_context=True)
    async def move(self, ctx, group, request):
        request = request.lower()
        members = []
        if group == "x":
            members = await get_favorite_members(ctx)
        else:
            r = re.search("<@(\d+)>", group)
            if not r:
                return
            members.append(ctx.message.server.get_member(r.group(1)))
        channels = self.client.get_all_channels()

        # allow partial matches, not efficient
        for channel in channels:
            if request in channel.name.lower():
                target = channel

        for member in members:
            await self.client.move_member(member, target)

    @auth_check()
    @commands.command(pass_context=True)
    async def kick(self, ctx):
        if not ctx.message.mentions:
            return
        for member in ctx.message.mentions:
            if get_user(member.id) == get_user(ctx.message.author):
                await self.client.say("Only super users can kick other global mods!")
                continue
            await self.client.kick(member)
            await self.client.say("Kicked {}! Request={}".format(member.name, ctx.message.author.name))

    @super_check()
    @commands.command(pass_context=True)
    async def ban(self, ctx):
        for member in ctx.message.mentions:
            await self.client.ban(member)
            await self.client.say("Banned {}! Request={}".format(member.name, ctx.message.author.name))

    @auth_check()
    @commands.command(pass_context=True)
    async def unban(self, ctx):
        for member in ctx.message.mentions:
            await self.client.unban(member)
            await self.client.say("Unbanned {}! Request={}".format(member.name, ctx.message.author.name))

    @super_check()
    @commands.command(pass_context=True)
    async def clear(self, ctx, i=2):
        i = int(i)
        await clear_internal(self.client, ctx.message.channel, i)

    @super_check()
    @commands.command(pass_context=True)
    async def add(self, ctx, mention, rank):
        for member in ctx.message.mentions:
            r = set_user(member.id, rank)
            if not r:
                await self.client.say("Failed to add user!")
                return
            await self.client.say("Added user {}".format(member.name))

    @commands.command(pass_context=True)
    async def allstats(self, ctx):
        members = get_all_users()
        max_star, max_time, max_count = await get_record_holders(members)
        text = "```ml\n"
        text += "{:<18}{:<10}{:<10}{:<10}{:<10}\n".format("Name", "Rank", "Stars", "Count", "Time")
        text += "{}\n".format('-' * 58)
        for name, rank, stars, message_count, time in members:
            member = ctx.message.server.get_member(name)
            time = str(int(round(time / 3600))) + " hrs"
            if name is max_star[0]:
                stars = "{}*".format(stars)

            if name is max_time[0]:
                time = "{}*".format(time)

            if name is max_count[0]:
                message_count = "{}*".format(message_count)

            if member.nick:
                name = member.nick
            else:
                name = member.name
            text += "{:<18}{:<10}{:<10}{:<10}{:<10}\n".format(name, rank, stars, message_count, time)
        text += "```\n"
        await self.client.say(text)

    @super_check()
    @commands.command(pass_context=True)
    async def award_credits(self, ctx, mention):
        for member in ctx.message.mentions:
            set_user_stars(member.id)

    @super_check()
    @commands.command(pass_context=True)
    async def take_credits(self, ctx, mention):
        for member in ctx.message.mentions:
            take_user_stars(member.id)

    @commands.command(pass_context=True)
    async def stats(self, ctx):
        count = get_user_count(ctx.message.author.id)
        time = get_user_time(ctx.message.author.id)
        time = str(datetime.timedelta(seconds=time))
        text = "```\n"
        text += "You have posted {} time(s) and spent {} in Safe Space\n".format(count, time)
        text += "```\n"
        await self.client.say(text)

    @super_check()
    @commands.command(pass_context=True)
    async def sync(self, ctx):
        await self.client.say("Now Syncing, this may take awhile but you already know that ben you fucking idiot")
        count = 0
        async for x in self.client.logs_from(ctx.message.channel, limit=500000):
            set_user_count(x.author.id)
            count += 1
        await self.client.say("Synced {} messages".format(count))


def setup(client):
    client.add_cog(Commands(client))
