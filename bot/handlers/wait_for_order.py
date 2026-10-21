# Хендлер подтверждения заказа
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.domain.pizza_mapping import DRINKS_MAPPING
from bot.keyboards.pizza_kb import DrinksCallback, get_wait_order_menu
from bot.states.order import OrderState

router = Router()


@router.callback_query(OrderState.wait_for_drinks, DrinksCallback.filter())
async def wait_for_order_handler(
    callback: CallbackQuery, callback_data: DrinksCallback, state: FSMContext
) -> None:
    data = await state.get_data()
    pizza_name = data.get("pizza_name", "Не выбрана")
    pizza_size = data.get("pizza_size", "Не выбран")
    drinks = DRINKS_MAPPING.get(callback_data.name, "Не выбран")

    await state.update_data(drinks=drinks)
    await state.set_state(OrderState.wait_for_order)
    await callback.answer()

    await callback.message.edit_text(
        text=f"Подтвердите ваш заказ.\n🍕 Пицца: {pizza_name}\n📐Размер: {pizza_size}\n🥤Напиток:{drinks}.",
        reply_markup=get_wait_order_menu(),
    )
