from core import HelperBot, Cog
import asyncio, discord
from random import choice
from datetime import datetime

with open("data/quotes.txt") as f:
    quotes = f.read().split('\n')


class OnMessage(Cog):
    def __init__(self, bot: HelperBot):
        self.bot = bot

    @Cog.listener("on_message")
    async def sector_17(self, message: discord.Message):
        if not message.guild: return
        if message.channel.id != 836874738609553459: return

        created: datetime = message.author.created_at
        joined: datetime = message.author.joined_at

        seconds = (created - joined).total_seconds()
        if seconds >= 86400:
            try:
                await message.author.remove_roles(discord.Object(id=851837681688248351), reason="Account age crosses 1d")
            except discord.Forbidden:
                pass

def setup(bot):
    bot.add_cog(OnMessage(bot))
