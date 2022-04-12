from __future__ import annotations
import functools

from discord.ext import commands
import discord
import typing


__all__ = ("Context", )


class Context(commands.Context):
    """A custom implementation of commands.Context class."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "{0.__class__.__name__}".format(self)

    @property
    def session(self) -> typing.Any:
        return self.bot.http_session

    @discord.utils.cached_property
    def replied_reference(self) -> typing.Optional[discord.Message]:
        ref = self.message.reference
        if ref and isinstance(ref.resolved, discord.Message):
            return ref.resolved.to_reference()
        return None

    @property
    def command_syntax(self):
        command = self.command
        ctx = self
        return (
            f"{ctx.clean_prefix}{command.qualified_name}{'|' if command.aliases else ''}"
            f"{'|'.join(command.aliases if command.aliases else '')} {command.signature}"
        )

    def with_type(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            context = args[0] if isinstance(args[0], commands.Context) else args[1]
            try:
                async with context.typing():
                    await func(*args, **kwargs)
            except discord.Forbidden:
                await func(*args, **kwargs)

        return wrapped

    async def show_help(self, command=None):
        cmd = self.bot.get_command("help")
        command = command or self.command.qualified_name
        await self.invoke(cmd, command=command)

    async def send(
        self, content: typing.Optional[str] = None, **kwargs
    ) -> typing.Optional[discord.Message]:
        perms = self.channel.permissions_for(self.me)
        if not (perms.send_messages and perms.embed_links):
            try:
                await self.author.send(
                    "Bot don't have either Embed Links/Send Messages permission in that channel. Please give sufficient permissions to the bot."
                )
            except discord.Forbidden:  # DMs locked
                pass
            return

        return await super().send(content, **kwargs)

    async def reply(self, content: typing.Optional[str] = None, **kwargs):
        perms = self.channel.permissions_for(self.me)
        if not (perms.send_messages and perms.embed_links):
            try:
                await self.author.send(
                    "Bot don't have permission to send message in that channel. Please give me sufficient permissions to do so."
                )
            except discord.Fobidden:
                pass
            return
        return await super().reply(content, **kwargs)