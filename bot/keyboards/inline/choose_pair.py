from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.services import orders

def builder(pairs: dict[str, dict[str, any]]) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    for pair in pairs.values():
        current_pair = orders.Pair(pair)
        current_pair.calculate_exchange_rate()

        builder.button(
            text=f"{current_pair.client_value} {current_pair.client_cur_title} — {current_pair.co_value} {current_pair.co_cur_title}",
            callback_data=f"{current_pair.co_cur_name}")

    builder.adjust(1)

    return builder
