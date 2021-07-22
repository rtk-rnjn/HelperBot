async def _create_tag(con, cur, db_name, name, _id, text):
    data = await cur.execute(
        '''INSERT INTO {} VALUES(?, ?, ?)'''.format(db_name),
        (name, _id, text))
    await con.commit()
    return data


async def _update_tag_name(con, cur, db_name, name, _id, text):
    data = await cur.execute(
        '''UPDATE {} SET name="{}" WHERE id={} name="{}"'''.format(
            db_name, text, _id, name))
    await con.commit()
    return data


async def _update_tag_text(con, cur, db_name, name, _id, text):
    data = await cur.execute(
        '''UPDATE {} SET text="{}" WHERE id={} name="{}"'''.format(
            db_name, text, _id, name))
    await con.commit()
    return data


async def _delete_tag(con, cur, db_name, name, _id):
    data = await cur.execute(
        '''DELETE FROM {} WHERE name="{}" AND id={}'''.format(
            db_name, name, _id))
    await con.commit()
    return data


async def _tranfer_tag_ownership(con, cur, db_name, name, _id, member_id):
    data = await cur.execute(
      '''UPDATE {} SET id={} WHERE name="{}" AND id={}'''.format(
        db_name, member_id, name, _id
      )
    )
    await con.commit()
    return data
