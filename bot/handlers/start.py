from aiogram import Router, types
from aiogram.filters import Command
from bot.services.users import UserService
from sqlalchemy.ext.asyncio import AsyncSession

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, session: AsyncSession):
    """
    Starts the bot
    Triggered by /start command
    Shows welcome message
    """

    user_service = UserService(session)
    await user_service.set_user(
        tg_id=message.from_user.id,
        name=message.from_user.full_name
    )
    await message.answer(f"""
Вітаємо, <b>{message.from_user.full_name}</b>!
Exchange bot - швидкий обмін криптовалют
Обмінюйте USDT, Bitcoin та більше 500 альткоїнів швидко, легко та безпечно

Для початку обміну, натисніть /exchange
""", parse_mode="HTML")
