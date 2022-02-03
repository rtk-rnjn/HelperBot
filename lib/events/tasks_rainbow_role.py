import discord, asyncio
from core import HelperBot, Cog
from discord.ext import tasks
import random
color = [16678812, 6670804, 13942761]
class RainbowRole(Cog):
    def __init__(self, bot: HelperBot):
        self.bot = bot
        self.RainbowRole.start()
        self.rain_bow_role = None
        self.not_your_role = None

    @tasks.loop(seconds=600)
    async def RainbowRole(self):
        await self.bot.wait_until_ready()
        if self.rain_bow_role is None:
            role = discord.utils.get(self.bot.get_guild(741614680652644382).roles,
                                     name='RainbowRole')
            self.rain_bow_role = role
        if self.rain_bow_role:
            await self.rain_bow_role.edit(
                colour=discord.Colour.random(),
                reason="Action featured by !! Ritik Ranjan [*.*]#9230")
        if self.not_your_role is None:
            roles = self.bot.get_guild(741614680652644382).roles
            for role in roles:
                if role.id == 884077440983511091:
                    self.not_your_role = role
                    break
        if self.not_your_role:
            await self.not_your_role.edit(colour=random.choice(color), reason="Action featured by !! Ritik Ranjan [*.*]#9230")

def setup(bot):
    bot.add_cog(RainbowRole(bot))
