# Хендлер обрабатывает нажатие кнопки назад

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.keyboards.pizza_kb import (
    DrinksCallback,
    OrderCallback,
    PizzaSizeCallback,
    get_drinks_menu,
    get_pizza_name_menu,
    get_pizza_size_menu,
)
from bot.states.order import OrderState

router = Router()


@router.callback_query(
    OrderState.wait_for_pizza_size,
    PizzaSizeCallback.filter(F.name == "back_to_pizza_name"),
)
async def back_to_pizza_name_handler(
    callback: CallbackQuery, state: FSMContext
) -> None:
    await state.set_state(OrderState.wait_for_pizza_name)
    await callback.answer()
    await callback.message.edit_text(
        text="🍕 Вы вернулись назад. Выберите пиццу из меню ниже:",
        reply_markup=get_pizza_name_menu(),
    )


@router.callback_query(
    OrderState.wait_for_drinks,
    DrinksCallback.filter(F.name == "back_to_pizza_size"),
)
async def back_to_pizza_size_handler(
    callback: CallbackQuery, state: FSMContext
) -> None:
    await state.set_state(OrderState.wait_for_pizza_size)
    await callback.answer()

    data = await state.get_data()
    pizza_name = data.get("pizza_name", "Выбранная пицца")

    await callback.message.edit_text(
        text=f"Вы вернулись назад.\n🍕 Пицца: {pizza_name}\n📐 Выберите размер пиццы:",
        reply_markup=get_pizza_size_menu(),
    )


@router.callback_query(
    OrderState.wait_for_order,
    OrderCallback.filter(F.name == "back_to_drinks"),
)
async def back_to_drinks_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(OrderState.wait_for_drinks)
    await callback.answer()

    data = await state.get_data()
    pizza_name = data.get("pizza_name", "Не выбрана")
    pizza_size = data.get("pizza_size", "Не выбран")

    await callback.message.edit_text(
        text=f"Вы вернулись назад.\n🍕Пицца: {pizza_name}\n📐Размер: {pizza_size}\n🥤Выберите пожалуйста напиток:",
        reply_markup=get_drinks_menu(),
    )
