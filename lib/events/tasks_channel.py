from __future__ import annotations

from core import HelperBot, Cog
from discord.ext import tasks
from random import choice

from utils.config import GENERAL, VOICE_GENERAL

with open("data/adj.txt") as f:
    adj = f.read().split("\n")

with open("data/topic.txt") as g:
    topic = g.read().split("\n")

with open("data/mr_robot.txt") as h:
    title = h.read().split("\n")


class ChannelBow(Cog):
    def __init__(self, bot: HelperBot):
        self.bot = bot
        self.ChannelBow.start()

    @tasks.loop(seconds=7200)
    async def ChannelBow(self):
        await self.bot.wait_until_ready()
        await self.bot.get_channel(GENERAL).edit(
            name=f"│\N{SPEECH BALLOON}│{choice(adj)}-general",
            reason="Action featured by !! Ritik Ranjan [*.*]",
        )
        await self.bot.get_channel(VOICE_GENERAL).edit(
            name=f"{choice(title)}", reason="Action featured by !! Ritik Ranjan [*.*]"
        )


async def setup(bot):
    await bot.add_cog(ChannelBow(bot))
