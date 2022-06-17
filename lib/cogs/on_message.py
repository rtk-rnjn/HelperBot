from __future__ import annotations
from contextlib import suppress

from core import HelperBot, Cog
import discord

from datetime import datetime

from utils.config import QU_ROLE, SECTOR_17


class OnMessage(Cog):
    def __init__(self, bot: HelperBot):
        self.bot = bot

    @Cog.listener("on_message")
    async def sector_17(self, message: discord.Message):
        if getattr(message.guild, "id", None) != SECTOR_17:
            return

        created: datetime = message.author.created_at
        joined: datetime = message.author.joined_at

        seconds = (created - joined).total_seconds()
        if seconds >= 86400 and message.author._roles.has(QU_ROLE):
            with suppress(discord.HTTPException):
                await message.author.remove_roles(
                    discord.Object(id=QU_ROLE),
                    reason="Account age crosses 1d",
                )


async def setup(bot):
    await bot.add_cog(OnMessage(bot))
