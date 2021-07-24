from core import HelperBot, Context, Cog
from discord.ext import commands

from . import method as mt 
from discord import Member
from .method import collection

class Tags(Cog):
    """Tag system for SECTOR 17-29"""
    def __init__(self, bot: HelperBot):    
        self.bot = bot

    @commands.group()
    async def tag(self, ctx: Context):
        """To make tags. Tags are cool"""
        pass

    @tag.command(name='create')
    async def create_tag(self, ctx: Context, name: commands.clean_content, *,
                         text: commands.clean_content):
        """To create a tag"""
        await mt._create_tag(name, ctx.author.id, text)

    @tag.command(name='delete')
    async def delete_tag(self, ctx: Context, name: commands.clean_content):
        """To delete a tag you own"""
        data = collection.find_one({'_id': name, 'owner': ctx.author.id})
        if not data: return
        await mt._delete_tag(name)

    @tag.command(name='editname')
    async def edit_tag_name(self, ctx: Context, name: commands.clean_content,
                            text: commands.clean_content):
        """To edit the name of tag you own"""
        data = collection.find_one({'_id': name, 'owner': ctx.author.id})
        if not data: return
        await mt._update_tag_name(name, text)

    @tag.command(name='edittext')
    async def edit_tag_text(self, ctx: Context, name: commands.clean_content,
                            *, text: commands.clean_content):
        """To edit the content of tag you own"""
        data = collection.find_one({'_id': name, 'owner': ctx.author.id})
        if not data: return
        await mt._update_tag_text(name, text)
    
    @tag.command(name='transferownership', aliases=['to'])
    async def tag_transfer(self, ctx: Context, name: commands.clean_content, *, member: Member):
        """To tansfer the tag ownership"""
        data = collection.find_one({'_id': name, 'owner': ctx.author.id})
        if not data: return
        await mt._tranfer_tag_ownership(name, member.id)

    @tag.command(name='show')
    async def show_tag(self, ctx: Context, name: commands.clean_content):
        """To show the tag"""
        data = collection.find_one({'_id': name})
        if not data: return
        await ctx.message.delete()
        await ctx.send(f"{data['text']}")
  
def setup(bot):
    bot.add_cog(Tags(bot))
