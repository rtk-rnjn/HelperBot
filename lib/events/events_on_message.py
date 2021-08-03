import discord
from discord.ext import commands
from core import Cog, HelperBot


class OnMessageMod(Cog):
    def __init__(self, bot: HelperBot):
        self.bot = bot
        self.channel = None
        self.cd_mapping = commands.CooldownMapping.from_cooldown(5, 5, commands.BucketType.member)

    @Cog.listener()
    async def on_message(self, message):
        await self.bot.wait_until_ready()
        if message.author.bot: return
        bucket = self.cd_mapping.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            await message.channel.send("rate limited 1") # rate limited
        else:
            pass #await message.channel.send("rate limited 2") # not rate limited
        if self.channel is None:
            self.channel = self.bot.get_channel(837637146453868554)

        if str(message.channel.type) == 'private':
            await self.channel.send(
                f"**{message.author.name}#{message.author.discriminator} ({message.author.id})**: {message.content}"
            )

        if message.channel is self.channel:
            if str(message.content).startswith('<'):
                user = message.mentions[0]
                await user.send(
                    f"**{message.author.name}#{message.author.discriminator}**: {message.content}"
                )


def setup(bot):
    bot.add_cog(OnMessageMod(bot))
