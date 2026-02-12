from aiogram.fsm.state import State, StatesGroup

class Order(StatesGroup):
    currency = State()
    pair = State()
    value = State()
    name = State()
    phone = State()
    email = State()
    to_acc = State()
    from_acc = State()
    create_order = State()
