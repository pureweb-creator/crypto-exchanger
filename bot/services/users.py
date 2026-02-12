from bot.database.database import session_maker
from bot.database.models import User
from sqlalchemy import select

async def set_user(tg_id: int, name: str, phone: str = None, email: str = None):
    async with session_maker() as session:
        user = await session.scalar(select(User).where(User.id == tg_id))

        if not user:
            new_user = User(id=tg_id, full_name=name, phone=phone, email=email)
            session.add(new_user)
            await session.commit()
        else:
            user.full_name = name
            await session.commit()

async def get_user(tg_id: int):
    async with session_maker() as session:
        return await session.scalar(select(User).where(User.id == tg_id))

async def update_user_email(tg_id: int, new_email: str):
    async with session_maker() as session:
        user = await session.scalar(select(User).where(User.id == tg_id))

        if user.email != new_email:
            user.email = new_email
            await session.commit()
        else:
            await session.rollback()

async def update_user_phone(tg_id: int, new_phone: str):
    async with session_maker() as session:
        user = await session.scalar(select(User).where(User.id == tg_id))

        if user.phone != new_phone:
            user.phone = new_phone
            await session.commit()
        else:
            await session.rollback()

async def update_user_name(tg_id: int, new_name: str):
    async with session_maker() as session:
        user = await session.scalar(select(User).where(User.id == tg_id))

        if user.full_name != new_name:
            user.full_name = new_name
            await session.commit()
        else:
            await session.rollback()
