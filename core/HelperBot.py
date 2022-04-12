
from .Context import Context
from discord.ext import commands
import discord, traceback, jishaku
from utils.config import EXTENTIONS, TOKEN
import aiohttp

from aiohttp import AsyncResolver, ClientSession, TCPConnector
import socket
import os

os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"


class HelperBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(command_prefix=self.get_prefix,
                         case_insensitive=False,
                         intents=discord.Intents.all(),
                         strip_after_prefix=True,
                         activity=discord.Activity(
                             type=discord.ActivityType.listening,
                             name="Parrot"),
                         status=discord.Status.idle,
                         **kwargs)
        self.http_session = ClientSession(
            connector=TCPConnector(resolver=AsyncResolver(), family=socket.AF_INET)
        )
        self._BotBase__cogs = commands.core._CaseInsensitiveDict()

    def run(self):
        super().run(TOKEN, reconnect=True)

    async def on_ready(self):
        print(
            f"[HelperBot] {self.user} ready to take commands"
        )

    async def process_commands(self, message: discord.Message):
        ctx = await self.get_context(message, cls=Context or commands.Context)
        
        if ctx.command is None:
            # ignore if no command found
            return
        await self.invoke(ctx)

    async def setup_hool(self):
        for ext in EXTENTIONS:
            try:
                self.load_extension(ext)
                print(f"[EXTENSION] {ext} was loaded successfully!")
            except Exception as e:
                tb = traceback.format_exception(type(e), e, e.__traceback__)
                tbe = "".join(tb) + ""
                print(f"[WARNING] Could not load extension {ext}: {tbe}")

    async def on_message(self, message: discord.Message):
        if not message.guild:
            return

        await self.process_commands(message)

    async def get_prefix(self, message: discord.Message) -> str:
        return commands.when_mentioned_or('H!', 'h!', '!H', '!h')(self, message)

    async def invoke_help_command(self, ctx: Context) -> None:
        return await ctx.send_help(ctx.command)