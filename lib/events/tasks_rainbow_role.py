import discord
from core import HelperBot, Cog
from discord.ext import tasks


class RainbowRole(Cog):
    def __init__(self, bot: HelperBot):
        self.bot = bot
        self.RainbowRole.start()

    @tasks.loop(seconds=10.0)
    async def RainbowRole(self):
        guild = self.bot.get_guild(741614680652644382)
        role = discord.utils.get(guild.roles, name='RainbowRole')
        if not role: return
        await role.edit(colour=discord.Colour.random(),
                        reason="Action featured by !! Ritik Ranjan [*.*]#9230")
        return


def setup(bot):
    bot.add_cog(RainbowRole(bot))
