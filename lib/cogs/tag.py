from core import HelperBot, Context, Cog
from discord.ext import commands
from utils import db


class Tags(Cog):
    def __init__(self, bot: HelperBot):
        self.bot = bot

    async def _create_tag(self, con, cur, db_name, name, _id, text):
        data = await cur.execute(
            '''INSERT INTO {} VALUES(?, ?, ?)'''.format(db_name),
            (name, db_name, _id, text))
        await con.commit()
        return data

    async def _update_tag_name(self, con, cur, db_name, name, _id, text):
        data = await cur.execute(
            '''UPDATE {} SET name={} WHERE id={} name={}'''.format(
                db_name, text, _id, name))
        await con.commit()
        return data

    async def _update_tag_text(self, con, cur, db_name, name, _id, text):
        data = await cur.execute(
            '''UPDATE {} SET text={} WHERE id={} name={}'''.format(
                db_name, text, _id, name))
        await con.commit()
        return data

    async def _delete_tag(self, con, cur, db_name, name, _id):
        data = await cur.execute(
            '''DELETE FROM {} WHERE name={} AND id={}'''.format(
                db_name, name, _id))
        await con.commit()
        return data

    @commands.group()
    async def tag(self, ctx: Context):
        pass

    @tag.command(name='create')
    async def create_tag(self, ctx: Context, name: commands.clean_content, *,
                         text: commands.clean_content):
        async with db.connect('data/db.db') as conn:
            async with conn.cursor() as cursor:
                try:
                    await self._create_tag(conn, cursor, 'tags', name,
                                           ctx.author.id, text)
                    await ctx.send('OK')
                except Exception as e:
                    await ctx.send(f'{e}')
            await conn.close()

    @tag.command(name='delete')
    async def delete_tag(self, ctx: Context, name: commands.clean_content, *,
                         text: commands.clean_content):
        async with db.connect('data/db.db') as conn:
            async with conn.cursor() as cursor:
                try:
                    await self._delete_tag(conn, cursor, 'tags', name,
                                           ctx.author.id)
                    await ctx.send('OK')
                except Exception as e:
                    await ctx.send(f'{e}')
            await conn.close()

    @tag.command(name='editname')
    async def edit_tag_name(self, ctx: Context, name: commands.clean_content,
                            text: commands.clean_content):
        async with db.connect('data/db.db') as conn:
            async with conn.cursor() as cursor:
                try:
                    await self._update_tag_name(conn, cursor, 'tags', name,
                                                ctx.author.id, text)
                    await ctx.send('OK')
                except Exception as e:
                    await ctx.send(f'{e}')
            await conn.close()

    @tag.command(name='edittext')
    async def edit_tag_text(self, ctx: Context, name: commands.clean_content,
                            *, text: commands.clean_content):
        async with db.connect('data/db.db') as conn:
            async with conn.cursor() as cursor:
                try:
                    await self._update_tag_text(conn, cursor, 'tags', name,
                                                ctx.author.id, text)
                    await ctx.send('OK')
                except Exception as e:
                    await ctx.send(f'{e}')
            await conn.close()


def setup(bot):
    bot.add_cog(Tags(bot))
