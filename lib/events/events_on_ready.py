import discord, asyncio, aiohttp
from core import Cog, HelperBot
from pytchat import LiveChatAsync
from datetime import datetime
import os

channel1 = os.environ['CHANNEL_1']
channel2 = os.environ['CHANNEL_2']


class OnReady(Cog):
    def __init__(self, bot: HelperBot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):

        livechat = LiveChatAsync("SpB6TJeRVLc")

        while livechat.is_alive():
            data = await livechat.get()

            async for c in data.async_items():
                footer = "Normal User"
                color = 16777215
                
                if c.author.isChatModerator: 
                    footer = "Chat Moderator"
                    color = 3447003
                if c.author.isChatOwner: 
                    footer = "Chat Owner"
                    color = 16705372
                date_obj = datetime.strptime(c.datetime, "%Y-%m-%d %H:%M:%S")

                data = {
                    'username': "Beasty Stats",
                    'avatar_url': "https://yt3.ggpht.com/ytc/AKedOLSsvX9K4ESvZt94SEKJg1Km6ufjYa_VUhbgXp6h=s176-c-k-c0x00ffffff-no-rj"
                }
                data['embeds'] = [{
                    'description': f"```\n{c.message}\n```",
                    'timestamp': date_obj.isoformat(),
                    'author': {
                        'name': f"{c.author.name}",
                        'url': f"{c.author.channelUrl}"
                    },
                    'thumbnail': {
                        'url': f"{c.author.imageUrl}"
                    },
                    'footer': {
                        'text': footer
                    },
                    'color': color 
                }]

                for hook in [
                        f'https://discord.com/api/webhooks/864089656701485066/{channel1}',
                        f'https://discord.com/api/webhooks/864089652410318850/{channel2}'
                ]:
                    async with aiohttp.ClientSession() as session:
                        async with session.post(hook, json=data) as response:
                            if response.status < 300:
                                break


def setup(bot):
    bot.add_cog(OnReady(bot))
