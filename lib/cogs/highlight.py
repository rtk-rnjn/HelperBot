
from __future__ import annotations
import os
from typing import Optional
from discord.ext import commands, tasks
import discord
import motor.motor_asyncio
from core import HelperBot, Cog, Context


my_secret = os.environ['DB_KEY']

cluster = motor.motor_asyncio.AsyncIOMotorClient(
    f"mongodb+srv://user:{str(my_secret)}@cluster0.xjask.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
)
db = cluster["highlight"]
collection = db["highlight"]

class Hightlight(Cog):
    def __init__(self, bot: HelperBot) -> None:
        self.bot = bot
        self.data = list()
        self.task.start()

    @commands.command(name='hadd')
    async def hadd(self, ctx: Context, *, phrase: str):
        """
        Adds a highlight word or phrase.

        Highlight words and phrases are not case-sensitive, so coffee, Coffee, and COFFEE will all notify you.
        When a highlight word is found, the bot will send you a private message with the message that triggered it along with context.

        To prevent abuse of the service, you can only have 10 highlight word or phrases.
        """
        if len(phrase) not in list(range(2, 41)):
            await ctx.send("Phrase lenght must not more than 40 or less than 2")
            return
        if data := await collection.find_one({'_id': ctx.author.id}):
            if len(data.get('word')) >= 10:
                return await ctx.send("Can not make more than 10", delete_after=3)
            else:
                await collection.update_one({'_id': ctx.author.id,}, {'$addToSet': {'word': phrase.lower()}})
                await ctx.send("Added that word in the list.", delete_after=3)
        else:
            await collection.insert_one({'_id': ctx.author.id, 'word': [phrase.lower()]})
            await ctx.send("Added that word in the list.", delete_after=3)
    
    @commands.command(name='hdel')
    async def hdel(self, ctx: Context, *, phrase: str):
        """
        Removes a previously registered highlight word or phrase.

        Highlight words and phrases are not case-sensitive,
        so coffee, Coffee, and COFFEE will all notify you.
        """
        if data := await collection.find_one({'_id': ctx.author.id}):
            await collection.update_one({'_id': ctx.author.id}, {'$pull': {'word': phrase.lower()}})
            await ctx.send("Removed that word from list, if existed")
        else:
            await ctx.send('You dont have any highlight words yet')

    @commands.command(name='hshow')
    async def hshow(self, ctx: Context):
        """Shows all your highlight words."""
        if data := await collection.find_one({'_id': ctx.author.id}):
            await ctx.send(f"Your words/phrase `{'`, `'.join(data['word'])}`")
        else:
            await ctx.send('You dont have any highlight words yet')
    
    @Cog.listener()
    async def on_message(self, message: discord.Message):
        await self.bot.wait_until_ready()
        if message.author.bot:
            return
        if message.guild is None:
            return

        for data in self.data:
            if message.content.lower() in data['word']:
                # if message.author.id != data['_id']:
                    embed = await self.make_embed(message, message.content)
                    await self.send_embed(data['_id'], embed)
    
    async def make_embed(self, message, text: str) -> Optional[discord.Embed]:
        ls = []
        async for msg in message.channel.history(
                            limit=5,
                        ):
            ls.append(f"[**{discord.utils.format_dt(msg.created_at)}**] {msg.author}: {msg.content.replace(text, f'**{text}**')}")
        embed = discord.Embed(timestamp=message.created_at, color=message.author.color)
        embed.description = '\n'.join(ls)
        embed.add_field(name='Jump URL', value=f"[Jump Url]({message.jump_url})")
        return embed
    
    async def send_embed(self, _id, embed):
        try:
            await self.bot.get_user(_id).send(embed=embed)
        except Exception as e:
            print(e)

    @tasks.loop(seconds=5)
    async def task(self):
        self.data = []
        async for data in collection.find({}):
            self.data.append(data)

def setup(bot):
    bot.add_cog(Hightlight(bot))