from core import HelperBot, Cog
import asyncio
from random import choice

with open("data/quotes.txt") as f:
    quotes = f.read().split('\n')


class OnMessage(Cog):
    def __init__(self, bot: HelperBot):
        self.bot = bot
        self.channel = self.bot.get_channel(796645162860150784)

    @Cog.listener()
    async def on_message(self, message):
        if not message.guild: return
        if message.channel.id != 836874738609553459: return
        
        if self.channel is None:
            self.channel = self.bot.get_channel(796645162860150784)

        def check(m):
            return m.author.id == 302050872383242240

        if message.content.lower() == "!d bump":
            try:
                msg_em = await self.bot.wait_for('message',
                                                 timeout=10.0,
                                                 check=check)
            except Exception:
                return

            if msg_em.embeds:
                des = msg_em.embeds[0].description
                if "bump done" in des.lower():
                    await asyncio.sleep(60 * 60 * 2)
                    await self.channel.send(
                        f"**{choice(quotes)}**\n\nBump Us at: {self.channel.mention}"
                    )


def setup(bot):
    bot.add_cog(OnMessage(bot))
