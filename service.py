from connection import *      


async def create_user(username, full_name, telegram_id):
    try:
        conn = await connection_db()
        await conn.execute("""
        insert into users(username, full_name, telegram_id) Values
        ($1, $2, $3) 
                     """, username, full_name,str(telegram_id))
    except Exception as Error:
        print(f"Create user Error: {Error}")
    finally:
        await conn.close()
        
        

async def get_user_by_id(telegram_id):
    try:
        conn = await connection_db()
        user = await conn.fetchrow("""
        select * from users where telegram_id = $1
                     """, str(telegram_id))
        return user
    except Exception as Error:
        print(f"Get user by id Error: {Error}")
    finally:
        await conn.close()
        

async def check_admin(telegram_id):
    try:
        conn = await connection_db()
        users = await conn.fetchrow("""
        select * from users where telegram_id = $1 and is_admin = true
                     """, str(telegram_id))
        return users
    except Exception as Error:
        print(f"Get user Error: {Error}")
    finally:
        await conn.close()
        
        
async def create_category_db(title):
    try:
        conn = await connection_db()
        await conn.execute("""
        insert into category(category_name)Values
        ($1) 
                     """, title)
        return True
    except Exception as Error:
        print(f"Create category Error: {Error}")
        return False
    finally:
        await conn.close()


async def get_category():
    try:
        conn = await connection_db()
        categorys = await conn.fetch("""
        select * from category
                     """)
        return categorys
    except Exception as Error:
        print(f"Get categorys by id Error: {Error}")
    finally:
        await conn.close()
        
        
        
        
        
        
async def create_dishes_db(category_id, name, caption, price, file_id):
    try:
        conn = await connection_db()
        await conn.execute("""
        insert into dishes(category_id, name, caption, price, file_id)Values
        ($1, $2, $3, $4, $5) 
                     """, int(category_id), name, caption, int(price), file_id)
        return True
    except Exception as Error:
        print(f"Create category Error: {Error}")
        return False
    finally:
        await conn.close()




async def get_dishes_cat_id(category_id):
    try:
        conn = await connection_db()
        dishes = await conn.fetch("""
        select * from dishes where category_id = $1
                     """, int(category_id))
        return dishes
    except Exception as Error:
        print(f"Get dishes by id Error: {Error}")
    finally:
        await conn.close()
        
async def get_dishes_id(dish_id):
    try:
        conn = await connection_db()
        dishe = await conn.fetchrow("""
        select * from dishes where dish_id = $1
                     """, int(dish_id))
        return dishe
    except Exception as Error:
        print(f"Get dishes by id Error: {Error}")
    finally:
        await conn.close()