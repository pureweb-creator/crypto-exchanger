from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.services import OrderService

def builder(
    pairs: dict[str, dict[str, any]]
) -> InlineKeyboardBuilder:

    builder = InlineKeyboardBuilder()

    for pair in pairs.values():
        order_service = OrderService()
        rate_in_value = order_service.calculate_rate_in_value(pair)
        rate_out_value = order_service.calculate_rate_out_value(pair)

        builder.button(
            text=f"{rate_in_value} {pair['ClientCurTitle']} — {rate_out_value} {pair['CoCurTitle']}",
            callback_data=f"{pair['CoCurName']}")

    builder.adjust(1)

    return builder
