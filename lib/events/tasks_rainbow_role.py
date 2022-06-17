import discord, asyncio
from core import HelperBot, Cog
from discord.ext import tasks
import random

from utils.config import RAINBOW_ROLE, SECTOR_17, SPECIAL_RAINBOW_ROLE
color = [16678812, 6670804, 13942761]
class RainbowRole(Cog):
    def __init__(self, bot: HelperBot):
        self.bot = bot
        self.RainbowRole.start()

        guild = self.bot.get_guild(SECTOR_17)

        self.rain_bow_role = guild.get_role(RAINBOW_ROLE)
        self.not_your_role = guild.get_role(SPECIAL_RAINBOW_ROLE)

    @tasks.loop(seconds=600)
    async def RainbowRole(self):
        await self.bot.wait_until_ready()

        if self.rain_bow_role:
            await self.rain_bow_role.edit(
                colour=discord.Colour.random(),
                reason="Action featured by !! Ritik Ranjan [*.*]#9230")

        if self.not_your_role:
            await self.not_your_role.edit(colour=random.choice(color), reason="Action featured by !! Ritik Ranjan [*.*]#9230")

async def setup(bot):
    await bot.add_cog(RainbowRole(bot))
