import discord, asyncio
from core import HelperBot, Cog
from discord.ext import tasks
from random import choice

with open('data/adj.txt') as f:
    adj = f.read().split('\n')

with open('data/topic.txt') as g:
    topic = g.read().split('\n')

with open('data/mr_robot.txt') as h:
    title = h.read().split('\n')


class ChannelBow(Cog):
    def __init__(self, bot: HelperBot):
        self.bot = bot
        self.ChannelBow.start()

    @tasks.loop(seconds=7200)
    async def ChannelBow(self):
        await self.bot.wait_until_ready()
        await self.bot.get_channel(796645162860150784).edit(name=f"│💬│{choice(adj)}-general", reason=f"Action featured by !! Ritik Ranjan [*.*]")
        await self.bot.get_channel(770691788960432169).edit(name=f'{choice(title)}', reason=f"Action featured by !! Ritik Ranjan [*.*]")


async def setup(bot):
    await bot.add_cog(ChannelBow(bot))
