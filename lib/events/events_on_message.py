import discord
from core import Cog, HelperBot


class OnMessageMod(Cog):
    def __init__(self, bot: HelperBot):
        self.bot = bot
        self.channel = self.bot.get_channel(837637146453868554)
    
    @Cog.listener()
    async def on_message(self, message):
        if message.guild or message.author.bot: return
        channel = self.channel
      
        if str(message.channel.type) == 'private':
            await channel.send(
                f"**{message.author.name}#{message.author.discriminator} ({message.author.id})**: {message.content}"
            )

        if message.channel is channel:
            if str(message.content).startswith('<'):
                user = message.mentions[0]
                await user.send(
                    f"**{message.author.name}#{message.author.discriminator}**: {message.content}"
                )


def setup(bot):
    bot.add_cog(OnMessageMod(bot))
