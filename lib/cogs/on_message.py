from core import HelperBot, Cog
import asyncio, discord
from random import choice
from datetime import datetime

with open("data/quotes.txt") as f:
    quotes = f.read().split('\n')


class OnMessage(Cog):
    def __init__(self, bot: HelperBot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message):
        if not message.guild: return
        if message.channel.id != 836874738609553459: return

        created: datetime = message.author.created_at
        joined: datetime = message.author.joined_at

        seconds = (created - joined).total_seconds()
        if seconds >= 86400:
            try:
                await message.author.remove_roles(discord.Object(id=851837681688248351), reason="Account age crosses 1d")
            except Exception:
                pass

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
                    await self.bot.get_channel(796645162860150784).send(
                        f"**{choice(quotes)}**\nBump Us at: <#836874738609553459>"
                    )


def setup(bot):
    bot.add_cog(OnMessage(bot))
