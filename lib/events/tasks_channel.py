import discord, asyncio
from core import HelperBot, Cog
from discord.ext import tasks
from random import choice

with open('data/adj.txt') as f:
    adj = f.read()

adj = adj.split('\n')

with open('data/topic.txt') as g:
    topic = g.read()

topic = topic.split('\n')


class ChannelBow(Cog):
    def __init__(self, bot: HelperBot):
        self.bot = bot
        self.ChannelBow.start()

    @tasks.loop(seconds=895)
    async def ChannelBow(self):
        await asyncio.sleep(5)
        channel = self.bot.get_channel(796645162860150784)
        await channel.edit(name=f"│💬│{choice(adj)}-general", reason=f"Action featured by !! Ritik Ranjan [*.*]")
        msg = channel.last_message
        if msg.author.id == self.bot.user.id: return
        await channel.send(f"{choice(topic)}")


def setup(bot):
    bot.add_cog(ChannelBow(bot))
