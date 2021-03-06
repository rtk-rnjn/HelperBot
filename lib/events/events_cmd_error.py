# -*- coding: utf-8 -*-

import discord, traceback, math, random
from discord.ext import commands
from datetime import datetime

from core import HelperBot, Context, Cog

with open("data/quotes.txt", encoding="utf-8") as f:
    quote = f.read()

quote = quote.split("\n")


class Cmd(Cog):
    """This category is of no use for you, ignore it."""

    def __init__(self, bot: HelperBot):
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        # if command has local error handler, return
        if hasattr(ctx.command, "on_error"):
            return

        # get the original exception
        error = getattr(error, "original", error)

        ignore = (commands.CommandNotFound, discord.Forbidden, discord.errors.NotFound)

        if isinstance(error, ignore):
            return

        if isinstance(error, commands.BotMissingPermissions):
            missing = [
                perm.replace("_", " ").replace("guild", "server").title()
                for perm in error.missing_perms
            ]
            if len(missing) > 2:
                fmt = "{}, and {}".format(", ".join(missing[:-1]), missing[-1])
            else:
                fmt = " and ".join(missing)
            _message = f"{random.choice(quote)}\n\nBot Missing permissions. Please provide the following permission(s) to the bot.```\n{fmt}```"
            return await ctx.send(_message)

        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(
                f"{random.choice(quote)}\n\nCommand On Cooldown. You are on command cooldown, please retry in **{math.ceil(error.retry_after)}**s."
            )

        if isinstance(error, commands.MissingPermissions):
            missing = [
                perm.replace("_", " ").replace("guild", "server").title()
                for perm in error.missing_perms
            ]
            if len(missing) > 2:
                fmt = "{}, and {}".format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = " and ".join(missing)
            _message = "{}\n\nMissing Permissions. You need the the following permission(s) to use the command.```\n{}```".format(
                random.choice(quote), fmt
            )
            await ctx.send(_message)
            return

        if isinstance(error, commands.MissingAnyRole):
            missing = [role for role in error.missing_roles]
            if len(missing) > 2:
                fmt = "{}, and {}".format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = " and ".join(missing)
            _message = "{}\n\nMissing Role. You need the the following role(s) to use the command.```\n{}```".format(
                random.choice(quote), fmt
            )
            await ctx.send(_message)
            return

        if isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.send(
                    f"{random.choice(quote)}\n\nNo Private Message. This command cannot be used in direct messages. It can only be used in server"
                )
            except discord.Forbidden:
                pass
            return

        if isinstance(error, commands.NSFWChannelRequired):
            em = discord.Embed(timestamp=datetime.utcnow())
            em.set_image(url="https://i.imgur.com/oe4iK5i.gif")
            await ctx.send(
                content=f"{random.choice(quote)}\n\nNSFW Channel Required. This command will only run in NSFW marked channel. https://i.imgur.com/oe4iK5i.gif",
                embed=em,
            )
            return

        if isinstance(error, commands.NotOwner):
            await ctx.send(
                f"{random.choice(quote)}\n\nNot Owner. You must have ownership of the bot to run {ctx.command.name}"
            )
            return

        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.send(
                f"{random.choice(quote)}\n\nPrivate Message Only. This comamnd will only work in DM messages"
            )

        elif isinstance(error, commands.BadArgument):
            if isinstance(error, commands.MessageNotFound):
                return await ctx.send(
                    f"{random.choice(quote)}\n\nMessage Not Found. Message ID/Link you provied is either invalid or deleted!"
                )
            if isinstance(error, commands.MemberNotFound):
                return await ctx.send(
                    f"{random.choice(quote)}\n\nMember Not Found. Member ID/Mention/Name you provided is invalid or bot can not see that Member"
                )
            if isinstance(error, commands.UserNotFound):
                return await ctx.send(
                    f"{random.choice(quote)}\n\nUser Not Found. User ID/Mention/Name you provided is invalid or bot can not see that User"
                )
            if isinstance(error, commands.ChannelNotFound):
                return await ctx.send(
                    f"{random.choice(quote)}\n\nChannel Not Found. Channel ID/Mention/Name you provided is invalid or bot can not see that Channel"
                )
            if isinstance(error, commands.RoleNotFound):
                return await ctx.send(
                    f"{random.choice(quote)}\n\nRole Not Found. Role ID/Mention/Name you provided is invalid or bot can not see that Role"
                )
            if isinstance(error, commands.EmojiNotFound):
                return await ctx.send(
                    f"{random.choice(quote)}\n\nEmoji Not Found. Emoji ID/Name you provided is invalid or bot can not see that Emoji"
                )

        elif isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(
                f"{random.choice(quote)}\n\nMissing Required Argument. Please use proper syntax.```\n[p]{ctx.command.name} {ctx.command.signature}```"
            )

        elif isinstance(error, commands.MaxConcurrencyReached):
            return await ctx.send(
                f"{random.choice(quote)}\n\nMax Concurrenry Reached. This command is already running in this server. You have wait for it to finish."
            )

        else:
            tb = traceback.format_exception(type(error), error, error.__traceback__)
            tbe = "".join(tb) + ""
            if len(tbe) < 1800:
                await ctx.send(
                    "Copy paste this error to `!! Ritik Ranjan [*.*]#9230`\n\n```py\nIgnoring exception in command {}: {}\n```".format(
                        ctx.command.name, tbe
                    )
                )


async def setup(bot):
    await bot.add_cog(Cmd(bot))
