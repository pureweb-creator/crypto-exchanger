from aiogram.utils.keyboard import InlineKeyboardBuilder

def builder(
    pairs: dict[str, dict[str, dict]],
    currencies: dict[str, dict[str, str]]
) -> InlineKeyboardBuilder:

    builder = InlineKeyboardBuilder()

    for key in pairs.keys():
        currency_title = currencies[key]['CurrencyTitle']
        builder.button(text=f"{currency_title}", callback_data=f"{key}")

    builder.adjust(2)

    return builder
