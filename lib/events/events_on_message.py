import discord, re, aiohttp
from datetime import datetime
from discord.ext import commands
from core import Cog, HelperBot

from utils import config

KEY = config.GOOGLE_KEY

class OnMessageMod(Cog):
    def __init__(self, bot: HelperBot):
        self.bot = bot
        self.channel = None
    
    async def channel_converter(self, arg):
        url = r"((http[s]?):\/\/)?(www\.|m\.)?(youtube|youtu)\.(com|be)\/(channel|c)\/[a-zA-Z0-9_-]{1,}"
        match = re.search(url, arg)
        if match:
            _id = arg.split("/")[-1]
            url = f"https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&id={_id}&key={KEY}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        res = await response.json()
                        return res
        match = re.search(r"[a-zA-Z0-9_-]{1,}", arg)
        if match:
            _id = match
            url = f"https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&id={arg}&key={KEY}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        res = await response.json()
                        return res


    @Cog.listener()
    async def on_message(self, message):
        await self.bot.wait_until_ready()
        if message.author.bot: return

        if self.channel is None:
            self.channel = self.bot.get_channel(837637146453868554)

        if str(message.channel.type) == 'private':
            await self.channel.send(
                f"**{message.author.name}#{message.author.discriminator} (`{message.author.id}`)**: {message.content}"
            )

        if message.channel is self.channel:
            if str(message.content).startswith('<'):
                user = message.mentions[0]
                await user.send(
                    f"**{message.author.name}#{message.author.discriminator}**: {message.content}"
                )
def setup(bot):
    bot.add_cog(OnMessageMod(bot))
