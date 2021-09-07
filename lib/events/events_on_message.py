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
        self.ignore_channel = {
            803486169861586965: True, # spam-channel
        }
        self.cd_mapping = commands.CooldownMapping.from_cooldown(
            10, 10, commands.BucketType.member)
    
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
                f"**{message.author.name}#{message.author.discriminator} ({message.author.id})**: {message.content}"
            )

        bucket = self.cd_mapping.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            if message.channel.id in self.ignore:
                pass
            else:
                await message.channel.send("Channel Rate limit is close to get triggered. Locking for 10sec", delete_after=10.1)
                await message.channel.edit(slowmode_delay=10, reason=f"Action featured by !! Ritik Ranjan [*.*] | Reason: 10 messages in less than 10 seconds")
                await asyncio.sleep(10)
                await message.channel.edit(slowmode_delay=0, reason=f"Action featured by !! Ritik Ranjan [*.*] | Reason: Slowmode Delay Expired")
                await message.channel.send("Channel Unlocked. All OK", delete_after=2)
        else:
            pass

        if message.channel is self.channel:
            if str(message.content).startswith('<'):
                user = message.mentions[0]
                await user.send(
                    f"**{message.author.name}#{message.author.discriminator}**: {message.content}"
                )
def setup(bot):
    bot.add_cog(OnMessageMod(bot))
