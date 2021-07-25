from discord.ext import commands
import discord, asyncio, time, datetime, aiohttp, json

from core import HelperBot, Context, Cog

with open('data/questions.json') as f:
  questions = json.load(f)

class ApplyMod(Cog):
    """This Section will only used in support server for asking for moderation!"""
    def __init__(self, bot: HelperBot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 900, commands.BucketType.user)
    async def applymod(self, ctx: Context):
        """
        Want mod? Consider asking us out!
        """
        #return await ctx.send("Mod application are closed for the time being")
        return
        await ctx.send(f"{ctx.author.mention} check your DM!", delete_after=3)

        try:
            message = await ctx.author.send("Hey there!")
            await asyncio.sleep(2)
            await message.edit(
                content="Please wait for few seconds to initiate!")
            await asyncio.sleep(5.5)
            await message.edit(content="Success")
            await asyncio.sleep(0.5)
            await message.delete()
        except Exception as e:
            return await ctx.send(
                "Can NOT DM the user. Make sure your DM(s) are turned. ```\nError: {}```"
                .format(e))

        start_msg = await ctx.author.send(
            "You have 5 mins to reply to each questions, else bot get asyncio.timeout Exception! Then try again later! If you changed your mind, and don't want to be the moderator then ignore this DM channel for 3 mins"
        )
        await asyncio.sleep(15)
        await start_msg.edit(
            content=
            "~~You have 5 mins to reply to each questions, else you will get the Timeout! Then try again later! If you changed your mind, and don't want to be the moderator then ignore this DM channel for 3 mins~~"
        )

        def check(m):
            return m.author == ctx.author and str(m.channel.type) == "private"

        ans = []

        main_ini = time.time()

        for question in questions:
            temp_time_ini = time.time()
            temp_msg = await ctx.author.send(f'{question}')
            try:
                msg = await self.bot.wait_for('message',
                                              timeout=300.0,
                                              check=check)
            except Exception:
                await ctx.author.send(
                    f"```\nError: You didn't answer on time.```")
                return await ctx.author.send(f"Try again after a while")

            temp_time_fin = time.time()
            ans.append(
                f"{msg.content}\n\nTime Taken: {round(temp_time_fin - temp_time_ini, 3)}s"
            )
            await temp_msg.edit(
                content=
                f'[QUESTION RETRACTED] Time taken to answer: `{round(temp_time_fin - temp_time_ini, 3)}`s'
            )

        main_fin = time.time()
        confirm_msg = await ctx.author.send("Please wait a seconds!")

        await asyncio.sleep(1)

        main_str = ""
        for q, a in zip(questions, ans):
            main_str = main_str + f"{q.replace('`', '')}\n{a}\n\n"

        channel = discord.utils.get(ctx.guild.channels, name='mod-application')
        try:
            async with aiohttp.ClientSession() as aioclient:
                post = await aioclient.post('https://hastebin.com/documents',
                                            data=main_str)
                if post.status == 200:
                    response = await post.text()
                    link = f'https://hastebin.com/{response[8:-2]}'
                    em = discord.Embed(
                        title="MODERATION APPLY",
                        description=
                        f"```\nNAME : {ctx.author.name}\nID   : {ctx.author.id}\nAT   : {datetime.datetime.utcnow()}\n\nTIME TAKEN : {round((main_fin - main_ini), 3)}```",
                        url=f"{link}")

                    await channel.send(embed=em)
                    await confirm_msg.edit(
                        content=
                        "Success! You will be notified ASAP! Thanks for your patience"
                    )
                    return

                post = await aioclient.post("https://bin.readthedocs.fr/new",
                                            data={
                                                'code': main_str,
                                                'lang': 'txt'
                                            })
                if post.status == 200:
                    link = post.url
                    em = discord.Embed(
                        title="MODERATION APPLY",
                        description=
                        f"```\nNAME : {ctx.author.name}\nID   : {ctx.author.id}\nAT   : {datetime.datetime.utcnow()}\n\nTIME TAKEN : {round((main_fin - main_ini), 3)}```",
                        url=f"{link}")

                    await channel.send(embed=em)
                    await confirm_msg.edit(
                        content=
                        "Success! You will be notified ASAP! Thanks for your patience"
                    )
                    return
        except Exception as e:
            await channel.send(f"Something not right!```\nError: {e}```\n{ans}"
                               )


def setup(bot):
    bot.add_cog(ApplyMod(bot))
