from aiogram.utils.keyboard import ReplyKeyboardBuilder

def builder(items: list[str], columns) -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()

    for item in items:
        builder.button(text=str(item))

    builder.adjust(columns)

    return builder
