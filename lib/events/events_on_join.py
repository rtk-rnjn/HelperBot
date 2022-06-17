from core import HelperBot, Cog
from discord import Embed 
from discord.utils import get
from discord.ext import tasks
from utils.config import FROM_GLOBAL_LINK, GENERAL, GLOBAL_LINK_CODE, QU_ROLE, RULES, SECTOR_17

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
            self.ping_channel = self.bot.get_channel(RULES)
        await self.ping_channel.send(f"{member.mention}", delete_after=1)
        if member.guild.id == SECTOR_17:
            current_count = get(await member.guild.invites(), code=GLOBAL_LINK_CODE).uses
            if (current_count - 1) == self.invite_count:
                await member.add_roles(self.inv, reason="Joined from Global Link")

            created = member.created_at
            today = member.joined_at

            guild = member.guild

            embed = Embed(
                title=
                f"{member} welcome to {member.guild.name}",
                description=f"We glad to see you here. Check out {self.ping_channel.mention} and enjoy!",
                timestamp=member.created_at)
            embed.set_thumbnail(url=f"{member.display_avatar.url}")
            embed.add_field(
                name="Account created at",
                value=f"<t:{int(created.timestamp())}:R>",
                inline=False)
            embed.set_footer(text=f"ID: {member.id}", icon_url=guild.icon.url)
            await self.channel.send(embed=embed)

            if (today - created).total_seconds() < 86400:
                await member.add_roles(self.sus, reason="Suspecious Account")

        self.invite_counter.start()
    
    @tasks.loop(count=1)
    async def invite_counter(self):
        await self.bot.wait_until_ready()
        guild = self.bot.get_guild(SECTOR_17)
        self.invite_count = get(await guild.invites(), code=GLOBAL_LINK_CODE).uses
        self.sus = guild.get_role(QU_ROLE)
        self.inv = guild.get_role(FROM_GLOBAL_LINK)
        self.channel = guild.get_channel(GENERAL)

async def setup(bot):
    await bot.add_cog(OnJoin(bot))
