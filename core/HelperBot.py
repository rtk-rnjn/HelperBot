from __future__ import annotations

from .Context import Context
from discord.ext import commands
import discord
import traceback
import jishaku  # type: ignore
from utils.config import EXTENTIONS, RITIK, TOKEN
import aiohttp  # type: ignore

import os

os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"


class HelperBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(
            command_prefix=self.get_prefix,
            case_insensitive=False,
            intents=discord.Intents.all(),
            strip_after_prefix=True,
            activity=discord.Activity(
                type=discord.ActivityType.listening, name="Parrot"
            ),
            status=discord.Status.idle,
            **kwargs,
        )
        self._BotBase__cogs = commands.core._CaseInsensitiveDict()
        self.__ready = False

    def run(self):
        super().run(TOKEN, reconnect=True)

    async def on_ready(self):
        if not self.__ready:
            await self.__setup_hook()
            self.__ready = True

        print(f"[HelperBot] {self.user} ready to take commands")

    async def process_commands(self, message: discord.Message):
        ctx = await self.get_context(message, cls=Context)

        if ctx.command is None:
            # ignore if no command found
            return
        await self.invoke(ctx)

    async def __setup_hook(self):
        for ext in EXTENTIONS:
            try:
                await self.load_extension(ext)
                print(f"[EXTENSION] {ext} was loaded successfully!")
            except Exception as e:
                traceback.print_exc()

    async def on_message(self, message: discord.Message):
        if not message.guild:
            return

        await self.process_commands(message)

    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.content != after.content and after.author.id == RITIK:
            await self.process_commands(after)

    async def get_prefix(self, message: discord.Message) -> str:
        return commands.when_mentioned_or("H!", "h!", "!H", "!h")(self, message)

    async def invoke_help_command(self, ctx: Context) -> None:
        return await ctx.send_help(ctx.command)
