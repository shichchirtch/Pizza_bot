from postgress_table import session_marker, User
from sqlalchemy import select, func

async def insert_new_user_in_table(user_tg_id: int, name: str):
    async with session_marker() as session:
        query = await session.execute(select(User).filter(User.tg_us_id == user_tg_id))
        needed_data = query.scalar()
        print('we are here')
        if not needed_data:
            print('Now we are into first function')
            new_us = User(tg_us_id=user_tg_id, user_name=name)
            session.add(new_us)
            await session.commit()


async def check_user_in_table(user_tg_id:int):
    """Функция проверяет есть ли юзер в БД"""
    async with session_marker() as session:
        print("Work check_user Function")
        query = await session.execute(select(User).filter(User.tg_us_id == user_tg_id))
        data = query.one_or_none()
        return data

async def insert_order(user_id: int):
    async with session_marker() as session:
        query = await session.execute(select(User).filter(User.tg_us_id == user_id))
        needed_data = query.scalar()
        if needed_data:
            needed_data.quantity_orders += 1
            await session.commit()


async def insert_total_summ(user_id:int, zakaz_summ:int):
    async with session_marker() as session:
        query = await session.execute(select(User).filter(User.tg_us_id == user_id))
        needed_data = query.scalar()
        needed_data.total_summ += zakaz_summ
        await session.commit()


async def return_total_summ(user_id:int):
    async with session_marker() as session:
        query = await session.execute(select(User).filter(User.tg_us_id == user_id))
        needed_data = query.scalar()
        return needed_data.total_summ

async def return_orders(user_id:int):
    async with session_marker() as session:
        query = await session.execute(select(User).filter(User.tg_us_id == user_id))
        needed_data = query.scalar()
        my_orders = needed_data.quantity_orders
        total = needed_data.total_summ
        return f'I have done already <b>{my_orders}</b> orders 🍕\nTotal summ: <b>{total}</b> 💶'

async def get_user_count():
    '''Функция считает общее количество запустивших бота'''
    async with session_marker() as session:
        result = await session.execute(select(func.count(User.index)))
        count = result.scalar()
        return count

async def return_tg_id():
    async with session_marker() as session:

        tg_ids = session.query(User.tg_us_id).all()
        print('tg_ids: ', tg_ids)
        return tg_ids
