import discord, re
from discord.ext import commands
from core import Cog, HelperBot

from utils import config

KEY = config.GOOGLE_KEY

class OnMessageMod(Cog):
    def __init__(self, bot: HelperBot):
        self.bot = bot
        self.channel = None
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
            return await message.channel.send("Rate limited is being hit")
        else:
            pass

        if message.channel is self.channel:
            if str(message.content).startswith('<'):
                user = message.mentions[0]
                await user.send(
                    f"**{message.author.name}#{message.author.discriminator}**: {message.content}"
                )
        
        if message.channel.id == 876795177178632192:
            channel = await self.channel_converter(message.content)
            thread = await message.create_thread(name=f"{message.author.name}#{message.author.discriminator}")
            await thread.join()
            await thread.send(f"**{message.author.name}#{message.author.discriminator}**: {message.content}")
            await message.delete(delay=10)
            
            try: channel['items']
            except KeyError:
                embed = discord.Embed(
                    title='Hmm...!',
                    description=
                    f"```ini\n[CHANNEL YOU ARE LOOKING FOR DO NOT EXISTS]\n```",
                    color=message.author.color,
                    timestamp=datetime.utcnow())
                embed.set_footer(
                    text=
                    f'Requested by: {message.author.name}#{message.author.discriminator}',
                    icon_url=message.author.avatar.url)
                return await thread.send(content=f"{message.author.mention}", embed=embed, delete_after=120)
            else:
                embed = discord.Embed(
                    title=channel['items'][0]['snippet']['title'],
                    description=
                        f"```\n{channel['items'][0]['snippet']['description']}\n```",
                    color=message.author.color,
                    timestamp=datetime.utcnow()) 
                embed.set_thumbnail(
                    url=f"{channel['items'][0]['snippet']['thumbnails']['default']['url']}")
                embed.set_footer(
                    text=f'Requested by: {message.author.name}#{message.author.discriminator}',
                    icon_url=message.author.avatar.url)
                embed.add_field(name="View Count", value=f"{channel['items'][0]['statistics']['viewCount']}", inline=True)
                embed.add_field(name="Sub Count", value=f"{channel['items'][0]['statistics']['subscriberCount']}", inline=True)
                embed.add_field(name="Video Count", value=f"{channel['items'][0]['statistics']['videoCount']}", inline=True)
                embed.add_field(name="Country", value=f"{channel['items'][0]['snippet']['country']}", inline=True)

                return await thread.send(content=f"{message.author.mention}", embed=embed, delete_after=120)

def setup(bot):
    bot.add_cog(OnMessageMod(bot))
