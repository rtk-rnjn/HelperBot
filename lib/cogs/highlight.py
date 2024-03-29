from __future__ import annotations

import re
from typing import Optional, Union
from discord.ext import commands, tasks
import discord
import motor.motor_asyncio  # type: ignore
from core import HelperBot, Cog, Context
from utils.config import DB_KEY

cluster = motor.motor_asyncio.AsyncIOMotorClient(
    f"mongodb+srv://user:{str(DB_KEY)}@cluster0.xjask.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
)
db = cluster["highlight"]
collection = db["highlight"]


class Hightlight(Cog):
    """A highlight system!"""

    def __init__(self, bot: HelperBot) -> None:
        self.bot = bot
        self.data = []
        self.task.start()

    def isin(self, phrase: str, sentence: str) -> bool:
        word = re.escape(phrase)
        pattern = rf"\b{word}\b"
        return re.search(pattern, sentence) is not None

    def word(self, list_of_phrase: str, sentence: str) -> bool:
        for phrase in list_of_phrase:
            word = re.escape(phrase)
            pattern = rf"\b{word}\b"
            if re.search(pattern, sentence) is not None:
                return word

    @commands.command(name="hadd")
    async def hadd(self, ctx: Context, *, phrase: str):
        """
        Adds a highlight word or phrase.

        Highlight words and phrases are not case-sensitive, so coffee, Coffee, and COFFEE will all notify you.
        When a highlight word is found, the bot will send you a private message with the message that triggered it along with context.

        To prevent abuse of the service, you can only have 10 highlight word or phrases.
        """
        if len(phrase) not in list(range(3, 41)):
            await ctx.send("Phrase lenght must not more than 40 or less than 3")
            return
        if data := await collection.find_one({"_id": ctx.author.id}):
            if len(data.get("words")) >= 10:
                return await ctx.send("Can not make more than 10", delete_after=3)
            await collection.update_one(
                {
                    "_id": ctx.author.id,
                },
                {"$addToSet": {"words": phrase.lower()}},
            )
        else:
            await collection.insert_one(
                {"_id": ctx.author.id, "words": [phrase.lower()]}
            )

        await ctx.send("Added that word in the list.", delete_after=3)

    @commands.command(name="hdel")
    async def hdel(self, ctx: Context, *, phrase: str):
        """
        Removes a previously registered highlight word or phrase.

        Highlight words and phrases are not case-sensitive,
        so coffee, Coffee, and COFFEE will all notify you.
        """
        if data := await collection.find_one({"_id": ctx.author.id}):
            await collection.update_one(
                {"_id": ctx.author.id}, {"$pull": {"words": phrase.lower()}}
            )
            await ctx.send("Removed that word from list, if existed")
        else:
            await ctx.send("You dont have any highlight words yet")

    @commands.command(name="hshow")
    async def hshow(self, ctx: Context):
        """Shows all your highlight words."""
        if data := await collection.find_one({"_id": ctx.author.id}):
            await ctx.send(f"Your words/phrase ``{'``, ``'.join(data['words'])}``")
        else:
            await ctx.send("You dont have any highlight words yet")

    @commands.command("hblock")
    async def hblock(
        self, ctx: Context, *, target: Union[discord.Member, discord.TextChannel] = None
    ):
        """Blockes the User or TextChannel from getting the highlight words"""
        if data := await collection.find_one({"_id": ctx.author.id}):
            await collection.update_one(
                {"_id": ctx.author.id}, {"$addToSet": {"blocked": target.id}}
            )
            await ctx.send(f"Added {target} to your blocked list")
        else:
            await ctx.send("You dont have any highligh words yet")

    @commands.command("hunblock")
    async def hblock(
        self, ctx: Context, *, target: Union[discord.Member, discord.TextChannel] = None
    ):
        """Unblockes the User or TextChannel from getting the highlight words"""
        if data := await collection.find_one({"_id": ctx.author.id}):
            await collection.update_one(
                {"_id": ctx.author.id}, {"$pull": {"blocked": target.id}}
            )
            await ctx.send(f"Removed {target} from your blocked list, if existed")
        else:
            await ctx.send("You dont have any highligh words yet")

    @Cog.listener()
    async def on_message(self, message: discord.Message):
        await self.bot.wait_until_ready()

        if message.author.bot:
            return

        if not message:
            return

        if message.guild is None:
            return

        for data in self.data:
            if message.author.id in data.get(
                "blocked", []
            ) or message.channel.id in data.get("blocked", []):
                return
            if message.author.id != data["_id"] and any(
                self.isin(content, message.content.lower()) for content in data["words"]
            ):
                word = self.word(data["words"], message.content.lower())
                embed = await self.make_embed(message, word)
                await self.send_embed(
                    data["_id"],
                    embed,
                    content=f"In {message.channel.mention} for server `{message.guild.name}`, you were mentioned with the highlight word **{word}**",
                )

    async def make_embed(self, message, text: str) -> Optional[discord.Embed]:
        ls = []
        async for msg in message.channel.history(
            limit=5,
        ):
            ls.append(
                f"[**{discord.utils.format_dt(msg.created_at, 'T')}**] {msg.author}: {msg.content.replace(text, f'**{text}**')}"
            )
        embed = discord.Embed(
            title=f"{text}", timestamp=message.created_at, color=message.author.color
        )
        ls.reverse()
        embed.description = "\n".join(ls)
        embed.add_field(name="Jump URL", value=f"[Jump Url]({message.jump_url})")
        return embed

    async def send_embed(self, _id, embed, *, content):
        try:
            await self.bot.get_user(_id).send(content=content, embed=embed)
        except Exception as e:
            print(e)

    @Cog.listener()
    async def on_command_completion(self, ctx: Context):
        if ctx.command.name in ["hadd", "hdel", "hshow", "hblock", "hunblock"]:
            await self.task.start()

    @tasks.loop()
    async def task(self):
        self.data = [data async for data in collection.find({})]


async def setup(bot):
    await bot.add_cog(Hightlight(bot))
