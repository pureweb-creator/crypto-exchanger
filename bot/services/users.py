from bot.database.models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class UserService():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def set_user(self, tg_id: int, name: str, phone: str = None, email: str = None):
        user = await self.session.scalar(select(User).where(User.id == tg_id))

        if not user:
            new_user = User(id=tg_id, full_name=name, phone=phone, email=email)
            self.session.add(new_user)
            await self.session.commit()
        else:
            user.full_name = name
            await self.session.commit()

    async def get_user(self, tg_id: int):
        return await self.session.scalar(select(User).where(User.id == tg_id))

    async def update_user_email(self, tg_id: int, new_email: str):
        user = await self.session.scalar(select(User).where(User.id == tg_id))

        if user.email != new_email:
            user.email = new_email
            await self.session.commit()

    async def update_user_phone(self, tg_id: int, new_phone: str):
        user = await self.session.scalar(select(User).where(User.id == tg_id))

        if user.phone != new_phone:
            user.phone = new_phone
            await self.session.commit()

    async def update_user_name(self, tg_id: int, new_name: str):
        user = await self.session.scalar(select(User).where(User.id == tg_id))

        if user.full_name != new_name:
            user.full_name = new_name
            await self.session.commit()
