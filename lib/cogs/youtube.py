from core import HelperBot, Cog, Context
import re, aiohttp, discord, json
from datetime import datetime
from discord.ext import commands
from utils import config, youtube_search, paginator

KEY = config.GOOGLE_KEY


class YouTube(Cog, name='youtube'):
    def __init__(self, bot: HelperBot):
        self.bot = bot

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


    @commands.command(aliases=['subs', 'subscriber'])
    @commands.guild_only()
    async def sub(self, ctx: Context, *, channel: str):
        """To get the sub count of a given URL"""
        channel = await self.channel_converter(channel)

        try: channel['items']
        except KeyError:
            embed = discord.Embed(
                title='Hmm...!',
                description=
                f"```\nCHANNEL YOU ARE LOOKING FOR WITH ID: {channel['id']} DO NOT EXISTS\n```",
                color=ctx.author.color,
                timestamp=datetime.utcnow())
            embed.set_footer(
                text=
                f'Requested by: {ctx.author.name}#{ctx.author.discriminator}',
                icon_url=ctx.author.avatar_url)
            return await ctx.send(content=f"{ctx.author.mention}", embed=embed)
        
        embed = discord.Embed(
            title=channel['items'][0]['snippet']['title'],
            description=
            f"```\n{channel['items'][0]['snippet']['description']}\n```",
            color=ctx.author.color,
            timestamp=datetime.utcnow()) 
        embed.set_thumbnail(
            url=f"{channel['items'][0]['snippet']['thumbnails']['default']['url']}")
        embed.set_footer(
            text=f'Requested by: {ctx.author.name}#{ctx.author.discriminator}',
            icon_url=ctx.author.avatar_url)
        embed.add_field(name="View Count", value=f"{channel['items'][0]['statistics']['viewCount']}", inline=True)
        embed.add_field(name="Sub Count", value=f"{channel['items'][0]['statistics']['subscriberCount']}", inline=True)
        embed.add_field(name="Video Count", value=f"{channel['items'][0]['statistics']['videoCount']}", inline=True)
        embed.add_field(name="Country", value=f"{channel['items'][0]['snippet']['country']}", inline=True)

        await ctx.send(content=f"{ctx.author.mention}", embed=embed)

    @commands.command(aliases=['yt'])
    async def youtube(self, ctx: Context, *, query: str):
        results = await youtube_search.YoutubeSearch(query, max_results=5).to_json()
        main = json.loads(results)

        em_list = []

        for i in range(0, len(main['videos'])):
            _1_title = main['videos'][i]['title']
            _1_descr = main['videos'][i]['long_desc']
            _1_chann = main['videos'][i]['channel']
            _1_views = main['videos'][i]['views']
            _1_urlsu = 'https://www.youtube.com' + str(
                main['videos'][i]['url_suffix'])
            _1_durat = main['videos'][i]['duration']
            _1_thunb = str(main['videos'][i]['thumbnails'][0])

            embed = discord.Embed(description=f"```\n{_1_descr}\n```",
                                  colour=ctx.author.color,
                                  timestamp=datetime.utcnow())
            embed.set_author(name=f'{_1_title}', url=f'{_1_urlsu}')

            embed.set_thumbnail(
                url=
                'https://cdn4.iconfinder.com/data/icons/social-messaging-ui-color-shapes-2-free/128/social'
                '-youtube-circle-512.png')
            embed.add_field(name="Channel", value=f"{_1_chann}", inline=True)
            embed.add_field(name="Views", value=f"{_1_views}", inline=True)
            embed.add_field(name="Duration", value=f"{_1_durat}", inline=True)
            embed.add_field(name="URL/LINK", value=f"{_1_urlsu}", inline=True)
            embed.set_image(url=f'{_1_thunb}')
            embed.set_footer(
                text=
                f'Requested by: {ctx.author.name}#{ctx.author.discriminator}',
                icon_url=ctx.author.avatar_url)
            em_list.append(embed)

        _paginator = paginator.Paginator(pages=em_list, timeout=60.0)
        await _paginator.start(ctx)


def setup(bot):
    bot.add_cog(YouTube(bot))
