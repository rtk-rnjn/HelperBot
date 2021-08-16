from core import HelperBot, Cog
from discord import Embed 
from discord.utils import get

class OnJoin(Cog):
    def __init__(self, bot: HelperBot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 741614680652644382:
            invites = await member.guild.invites()
            invite = get(invites, name='Foo')
            created = member.created_at
            today = member.joined_at

            timedelta = str(today - created).split(":")

            guild = member.guild

            embed = Embed(
                title=
                f"{member.name}#{member.discriminator} welcome to {member.guild.name}",
                description=
                "We glad to see you here. Check out <#785803322136592394> and enjoy!",
                timestamp=member.created_at)
            embed.set_thumbnail(url=f"{member.avatar.url}")
            embed.add_field(
                name="Account age",
                value=
                f"```{timedelta[0]} Hr(s) {timedelta[1]} Min(s) {timedelta[2]} Sec(s)```",
                inline=False)
            embed.set_footer(text=f"ID: {member.id}", icon_url=guild.icon.url)
            await self.bot.get_channel(796645162860150784).send(embed=embed)

            if (today - created).total_seconds() >= 86400: pass
            else:
                await member.add_roles(guild.get_role(851837681688248351),
                                       reason="Suspecious Account")

def setup(bot):
    bot.add_cog(OnJoin(bot))