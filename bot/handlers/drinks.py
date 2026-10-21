# Хендлер обрабатывает нажатие выбора размера пиццы
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.domain.pizza_mapping import PIZZA_SIZE_MAPPING
from bot.keyboards.pizza_kb import PizzaSizeCallback, get_drinks_menu
from bot.states.order import OrderState

router = Router()


@router.callback_query(OrderState.wait_for_pizza_size, PizzaSizeCallback.filter())
async def drinks_handler(
    callback: CallbackQuery, callback_data: PizzaSizeCallback, state: FSMContext
) -> None:
    data = await state.get_data()
    pizza_name = data.get("pizza_name", "Выбранная пицца")
    pizza_size = PIZZA_SIZE_MAPPING.get(callback_data.name, "Не выбран")

    await state.update_data(pizza_size=pizza_size)
    await state.set_state(OrderState.wait_for_drinks)

    await callback.answer()

    await callback.message.edit_text(
        text=f"🍕 Пицца: {pizza_name}\n📐Размер: {pizza_size}\n🥤Выберите пожалуйста напиток:",
        reply_markup=get_drinks_menu(),
    )
