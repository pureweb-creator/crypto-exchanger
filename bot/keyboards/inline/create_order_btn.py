from aiogram.utils.keyboard import InlineKeyboardBuilder

def builder() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Створити заявку",
        callback_data="create_order"
    )

    return builder.adjust(1)
