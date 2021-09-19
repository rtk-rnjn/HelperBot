from core import HelperBot, Cog
from discord import Embed 
from discord.utils import get
from discord.ext import tasks

class OnJoin(Cog):
    def __init__(self, bot: HelperBot):
        self.bot = bot
        self.invite_count = 0
        self.invite_counter.start()
        self.sus = None
        self.inv = None
        self.channel = None
        self.ping_channel = None
    
    @Cog.listener()
    async def on_member_join(self, member):
        await self.bot.wait_until_ready()
        if self.ping_channel is None:
            self.ping_channel = self.bot.get_channel(785803322136592394)
        await self.ping_channel.send(f"{member.mention}", delete_after=1)
        if member.guild.id == 741614680652644382:
            current_count = get(await member.guild.invites(), code="NEyJxM7G7f").uses
            if (current_count - 1) == self.invite_count:
                await member.add_roles(self.inv, reason="Joined from Either Stream or Support")

            created = member.created_at
            today = member.joined_at

            timedelta = str(today - created).split(":")

            guild = member.guild

            embed = Embed(
                title=
                f"{member.name}#{member.discriminator} welcome to {member.guild.name}",
                description="We glad to see you here. Check out <#785803322136592394> and enjoy!",
                timestamp=member.created_at)
            embed.set_thumbnail(url=f"{member.display_avatar.url}")
            embed.add_field(
                name="Account age",
                value=
                f"```{timedelta[0]} Hr(s) {timedelta[1]} Min(s) {timedelta[2]} Sec(s)```",
                inline=False)
            embed.set_footer(text=f"ID: {member.id}", icon_url=guild.icon.url)
            await self.channel.send(embed=embed)

            if (today - created).total_seconds() >= 86400: pass
            else:
                await member.add_roles(self.sus, reason="Suspecious Account")
        self.invite_counter.start()
    
    @tasks.loop(count=1)
    async def invite_counter(self):
        await self.bot.wait_until_ready()
        guild = self.bot.get_guild(741614680652644382)
        self.invite_count = get(await guild.invites(), code="NEyJxM7G7f").uses
        self.sus = guild.get_role(851837681688248351)
        self.inv = guild.get_role(876780196500484117)
        self.channel = guild.get_channel(796645162860150784)

def setup(bot):
    bot.add_cog(OnJoin(bot))
