from aiogram import Router, F
from aiogram import Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.states.order import Order
from bot.keyboards.inline import *
from bot.keyboards.reply import *
from bot.filters.pair_param_filter import AmountInRange
from bot.services import users, orders
from bot.core.redis_loader import redis_client as r
import json

router = Router()

@router.message(Command("exchange"))
async def cmd_exchange(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    First step
    Start the exchange process

    Triggered by /exchange command, loads pairs and currencies from Redis
    Presents initial keyboard with currencies
    """

    await state.clear()
    await state.set_state(Order.currency)

    pairs = json.loads(await r.get("exchange:pairs"))
    currencies = json.loads(await r.get("exchange:currencies"))

    await message.answer(
        "Виберіть валюту для обміну",
        reply_markup=choose_currency.builder(pairs['result'], currencies).as_markup(),
    )
    await bot.delete_message(message.chat.id, message.message_id)

@router.callback_query(Order.currency)
async def process_currency(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    """
    Second step

    Loads pairs for selected currency and presents keyboard with available pairs
    """

    await state.set_state(Order.pair)
    await state.update_data(
        message_id=callback.message.message_id,
        client_cur_name = callback.data
    )

    pairs = json.loads(await r.get("exchange:pairs"))
    filtered_pairs = pairs['result'][callback.data]

    await callback.message.answer(
        f"Виберіть напрям",
        reply_markup=choose_pair.builder(filtered_pairs).as_markup()
    )
    await callback.answer()

    await bot.delete_message(callback.message.chat.id, callback.message.message_id)

@router.callback_query(Order.pair)
async def process_pair(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    """
    Third step

    Loads selected pair from pairs by dictionary keys and saves to FSM Storage (Redis)

    Pairs structure:
        "result": {
            "USDTTRC20": {
                "SEPAEUR": {
                    "PairId": "11111",
                    ...,
                },
                ...,
            },
            ...,
        }
    Where,
    USDTTRC20 - currency name,
    SEPAEUR - available pair for given currency
    So selected pair would be pair['result']['key1']['key2']
    """

    await state.set_state(Order.value)

    data = await state.get_data()
    client_cur_name = data['client_cur_name']
    co_cur_name = callback.data
    pairs = json.loads(await r.get("exchange:pairs"))
    target_pair = pairs['result'][client_cur_name][co_cur_name]

    await state.update_data(
        pair_id=target_pair["PairId"],
        co_cur_after_int=target_pair["CoCurAfterInt"],
        co_cur_title=target_pair["CoCurTitle"],
        co_value=target_pair["CoValue"],
        base_value=target_pair["BaseValue"],
        client_cur_title=target_pair["ClientCurTitle"],
        co_cur_name=target_pair["CoCurName"],
        pair_param_min_amount=target_pair["PairParamMinAmount"],
        pair_param_max_amount=target_pair["PairParamMaxAmount"],
    )

    await callback.message.answer(
        f"""
Введіть суму {target_pair['ClientCurTitle']} для обміну
Мінімум: {target_pair['PairParamMinAmount']} {target_pair['ClientCurName']}
Максимум: {target_pair['PairParamMaxAmount']} {target_pair['ClientCurName']}"""
    )
    await callback.answer()

    await bot.delete_message(callback.message.chat.id, callback.message.message_id)

@router.message(Order.value, AmountInRange())
async def process_correct_value(message: Message, state: FSMContext) -> None:
    """
    Fourth step

    This handler fires if user sends correct amount to exchange
    AmountInRange() filter checks the value

    Calculates and saves amount of money user will get after exchange
    """

    await state.set_state(Order.name)
    await state.update_data(client_value=message.text)
    data = await state.get_data()

    co_value = await orders.calculate_co_value(data)

    await state.update_data(co_value=co_value)
    await message.answer(
        "Введіть ПІБ",
        reply_markup=simple_button.builder([message.from_user.full_name], 1).as_markup(
            resize_keyboard=True
        ),
    )

@router.message(Order.value)
async def process_worng_value(message: Message) -> None:
    """
    Fourth step
    Processes incorrect amount to exchange
    """

    await message.answer("Помилка. Ви ввели невірне число")

@router.message(Order.name)
async def process_name(message: Message, state: FSMContext) -> None:
    """
    Fifth step
    Saves user full name and asking to enter email on the next step
    """

    await state.set_state(Order.email)
    await state.update_data(name=message.text)

    await users.update_user_name(message.from_user.id, message.text)
    user = await users.get_user(message.from_user.id)

    if user.email is not None:
        await message.answer(
            "Введіть e-mail",
            reply_markup=simple_button.builder([user.email], 1).as_markup(
                resize_keyboard=True
            ),
        )
    else:
        await message.answer("Введіть e-mail", reply_markup=ReplyKeyboardRemove())

@router.message(Order.email, F.text.regexp(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}"))
async def process_correct_email(message: Message, state: FSMContext) -> None:
    """
    Sixth step
    Saves email and asks for a phone number or @revtag depending on currency
    """

    await state.set_state(Order.phone)
    await state.update_data(email=message.text)

    data = await state.get_data()
    user = await users.get_user(message.from_user.id)

    await users.update_user_email(message.from_user.id, message.text)

    co_cur_name = data["co_cur_name"]
    message_text = (
        "Введіть мітку рахунку (@revtag)"
        if co_cur_name.endswith("EUR")
        else "Введіть номер телефону"
    )
    reply_markup = (
        ReplyKeyboardRemove()
        if user.phone is None
        else simple_button.builder([user.phone], 1).as_markup(resize_keyboard=True)
    )

    await message.answer(message_text, reply_markup=reply_markup)

@router.message(Order.email)
async def process_worng_email(message: Message) -> None:
    """
    Sixth step
    Processes incorrect email
    """

    user = await users.get_user(message.from_user.id)
    wrong_email_message = "E-mail введено невірно. Будь ласка, спробуйте ще раз"

    if user.email is not None:
        await message.answer(
            wrong_email_message,
            reply_markup=simple_button.builder([user.email], 1).as_markup(
                resize_keyboard=True
            ),
        )
    else:
        await message.answer(wrong_email_message, reply_markup=ReplyKeyboardRemove())

@router.message(Order.phone)
async def process_phone(message: Message, state: FSMContext) -> None:
    """
    Seventh step
    Saves user phone number and asks for account on the next step
    """

    await state.set_state(Order.to_acc)
    await state.update_data(phone=message.text)

    await users.update_user_phone(message.from_user.id, message.text)
    await message.answer(
        "Введіть номер рахунку на який буде виплата",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(Order.to_acc)
async def process_to_acc(message: Message, state: FSMContext) -> None:
    """
    Eighth step
    Saves account from prev step
    Shows summary of an order and presents a button to confirm creating an order
    """

    await state.set_state(Order.create_order)
    await state.update_data(to_acc=message.text)

    data = await state.get_data()
    summary_text = f"""
<b>Підсумок</b>

Обмін {data['client_cur_title']} на {data['co_cur_title']}
Віддаєте {data['client_value']} {data['client_cur_name']}
Отримуєте {data['co_value']} {data['co_cur_name'][-3:]}
На рахунок {data['to_acc']}
ПІБ {data['name']}
Email {data['email']}
Телефон {data['phone']}

Увага! Курс буде зафіксовано тільки після створення заявки.
"""
    await message.answer(
        summary_text, parse_mode="HTML", reply_markup=create_order.builder().as_markup()
    )
