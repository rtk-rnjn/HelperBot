from core import HelperBot, Context, Cog
from discord.ext import commands
from utils import db
from . import method as mt 
from discord import Member
import sqlite3

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
        async with db.connect('data/db.db') as conn:
            async with conn.cursor() as cursor:
                try:
                    await mt._create_tag(conn, cursor, 'tags', name,
                                           ctx.author.id, text)
                    await ctx.send('OK')
                except Exception as e:
                    await ctx.send(f'{e}')
            await conn.close()

    @tag.command(name='delete')
    async def delete_tag(self, ctx: Context, name: commands.clean_content):
        """To delete a tag you own"""
        async with db.connect('data/db.db') as conn:
            async with conn.cursor() as cursor:
                try:
                    await mt._delete_tag(conn, cursor, 'tags', name,
                                           ctx.author.id)
                    await ctx.send('OK')
                except Exception as e:
                    await ctx.send(f'{e}')
            await conn.close()

    @tag.command(name='editname')
    async def edit_tag_name(self, ctx: Context, name: commands.clean_content,
                            text: commands.clean_content):
        """To edit the name of tag you own"""
        async with db.connect('data/db.db') as conn:
            async with conn.cursor() as cursor:
                try:
                    await mt._update_tag_name(conn, cursor, 'tags', name,
                                                ctx.author.id, text)
                    await ctx.send('OK')
                except Exception as e:
                    await ctx.send(f'{e}')
            await conn.close()

    @tag.command(name='edittext')
    async def edit_tag_text(self, ctx: Context, name: commands.clean_content,
                            *, text: commands.clean_content):
        """To edit the content of tag you own"""
        async with db.connect('data/db.db') as conn:
            async with conn.cursor() as cursor:
                try:
                    await mt._update_tag_text(conn, cursor, 'tags', name,
                                                ctx.author.id, text)
                    await ctx.send('OK')
                except Exception as e:
                    await ctx.send(f'{e}')
            await conn.close()
    
    @tag.command(name='transferownership', aliases=['to'])
    async def tag_transfer(self, ctx: Context, name: commands.clean_content, *, member: Member):
        """To tansfer the tag ownership"""
        async with db.connect('data/db.db') as conn:
            async with conn.cursor() as cursor:
                try:
                    await mt._tranfer_tag_ownership(conn, cursor, 'tags', name, ctx.author.id, member.id)
                    await ctx.send('OK')
                except Exception as e:
                    await ctx.send(f'{e}')
            await conn.close()

    @tag.command(name='show')
    async def show_tag(self, ctx: Context, name: commands.clean_content):
        """To show the tag"""
        async with ctx.channel.typing:
            conn = sqlite3.connect('data/db.db')
            cursor = conn.cursor()
            try:
              data = cursor.execute(f'''SELECT * FROM tags WHERE name={name}''')
              for data in data:
                  if not data: return 
                  else:
                    await ctx.send(f"{data[-1]}")
            except Exception as e:
                await ctx.send(f'{e}')
            conn.close()
  
def setup(bot):
    bot.add_cog(Tags(bot))
