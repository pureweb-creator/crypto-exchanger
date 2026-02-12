from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

class AmountInRange(Filter):
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        text = message.text.replace(',', '.')
        try:
            amount = float(text)
        except ValueError:
            return False

        data = await state.get_data()
        pair_param_min_amount = float(data['pair_param_min_amount'])
        pair_param_max_amount = float(data['pair_param_max_amount'])

        if pair_param_min_amount <= amount <= pair_param_max_amount:
            return True

        return False
