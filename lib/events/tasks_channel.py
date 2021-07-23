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

    @tasks.loop(seconds=7200)
    async def ChannelBow(self):
        await asyncio.sleep(5)
        channel = self.bot.get_channel(796645162860150784)
        await channel.edit(name=f"│💬│{choice(adj)}-general", reason=f"Action featured by !! Ritik Ranjan [*.*]")
        
        # await asyncio.sleep(5)
        # channel = self.bot.get_channel(803486169861586965)
        # await channel.edit(name=f"│🏁│{choice(adj)}-spam-here", reason=f"Action featured by !! Ritik Ranjan [*.*]")
        
        # await asyncio.sleep(5)
        # channel = self.bot.get_channel(836122084119674930)
        # await channel.edit(name=f"│💬│{choice(adj)}-beasty-stats", reason=f"Action featured by !! Ritik Ranjan [*.*]")

        # await asyncio.sleep(5)
        # channel = self.bot.get_channel(776420233832955934)
        # await channel.edit(name=f"│🤖│{choice(adj)}-bot-commands", reason=f"Action featured by !! Ritik Ranjan [*.*]")

        # await asyncio.sleep(5)
        # channel = self.bot.get_channel(781249690607288341)
        # await channel.edit(name=f"│🎰│{choice(adj)}-casino", reason=f"Action featured by !! Ritik Ranjan [*.*]")

        # await asyncio.sleep(5)
        # channel = self.bot.get_channel(794437999391408149)
        # await channel.edit(name=f"│🐸│{choice(adj)}-dank-memer", reason=f"Action featured by !! Ritik Ranjan [*.*]")
        
        # await asyncio.sleep(5)
        # channel = self.bot.get_channel(831548297956294686)
        # await channel.edit(name=f"│💍│{choice(adj)}-owo", reason=f"Action featured by !! Ritik Ranjan [*.*]")
        
        # await asyncio.sleep(5)
        # channel = self.bot.get_channel(789447984286400533)
        # await channel.edit(name=f"│🌳│{choice(adj)}-yggdrasil", reason=f"Action featured by !! Ritik Ranjan [*.*]")
        
        # await asyncio.sleep(5)
        # channel = self.bot.get_channel(832609885174628392)
        # await channel.edit(name=f"│🐈│{choice(adj)}-cutie", reason=f"Action featured by !! Ritik Ranjan [*.*]")
        
        # await asyncio.sleep(5)
        # channel = self.bot.get_channel(793362155788304414)
        # await channel.edit(name=f"│🌍│{choice(adj)}-global-chat", reason=f"Action featured by !! Ritik Ranjan [*.*]")

        # await asyncio.sleep(5)
        # channel = self.bot.get_channel(778174786643558440)
        # await channel.edit(name=f"│📽│{choice(adj)}-media", reason=f"Action featured by !! Ritik Ranjan [*.*]")

        # await asyncio.sleep(5)
        # channel = self.bot.get_channel(778174576449814548)
        # await channel.edit(name=f"│🖊│{choice(adj)}-quotes", reason=f"Action featured by !! Ritik Ranjan [*.*]")

        # await asyncio.sleep(5)
        # channel = self.bot.get_channel(784893862203883530)
        # await channel.edit(name=f"│🖋│{choice(adj)}-memes", reason=f"Action featured by !! Ritik Ranjan [*.*]")

        # await asyncio.sleep(5)
        # channel = self.bot.get_channel(793352530918506506)
        # await channel.edit(name=f"│🔢│{choice(adj)}-counting", reason=f"Action featured by !! Ritik Ranjan [*.*]")



def setup(bot):
    bot.add_cog(ChannelBow(bot))
