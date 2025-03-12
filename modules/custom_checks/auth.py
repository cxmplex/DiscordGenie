
from discord.ext import commands

from modules.database.db import get_user


def auth_check():
    def is_user_authenticated(ctx):
        return get_user(ctx.message.author.id) >= 3

    return commands.check(is_user_authenticated)


def super_check():
    def is_user_super(ctx):
        return get_user(ctx.message.author.id) == 4

    return commands.check(is_user_super)
