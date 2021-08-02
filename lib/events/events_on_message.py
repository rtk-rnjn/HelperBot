import discord
from core import Cog, HelperBot


class OnMessageMod(Cog):
    def __init__(self, bot: HelperBot):
        self.bot = bot
        self.channel = None

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

        if message.channel is self.channel:
            if str(message.content).startswith('<'):
                user = message.mentions[0]
                await user.send(
                    f"**{message.author.name}#{message.author.discriminator}**: {message.content}"
                )


def setup(bot):
    bot.add_cog(OnMessageMod(bot))
