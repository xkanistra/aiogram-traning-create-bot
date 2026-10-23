# Хендлер подтверждения заказа
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.domain.pizza_mapping import (
    DRINK_FIXED_PRICE,
    DRINKS_MAPPING,
    PIZZA_BASE_PRICES,
    PIZZA_SIZE_PRICES,
)
from bot.keyboards.pizza_kb import DrinksCallback, get_wait_order_menu
from bot.states.order import OrderState

router = Router()


async def show_order_confirmation_screen(message: Message, state: FSMContext) -> None:
    # Получаем сырые данные из FSM
    data = await state.get_data()

    pizza_key = data.get("pizza_name")
    size_key = data.get("pizza_size")
    drink_key = data.get("drinks")

    # Считаем цену
    pizza_price = PIZZA_BASE_PRICES.get(pizza_key, 0)
    size_price = PIZZA_SIZE_PRICES.get(size_key, 0)
    drink_price = 0 if drink_key == "none" else DRINK_FIXED_PRICE

    total_stars = pizza_price + size_price + drink_price

    # Сохраняем финальную стоимость в FSM, чтобы хэндлер оплаты её подхватил
    await state.update_data(total_price=total_stars)

    pizza_name = pizza_key if pizza_key else "Не выбрана"
    pizza_size = size_key if size_key else "Не выбран"
    drink_name = DRINKS_MAPPING.get(drink_key, "Не выбран")

    text = (
        f"🛒 *Ваш сформированный заказ:*\n\n"
        f"🍕 Пицца: `{pizza_name}` ({pizza_price} ⭐️)\n"
        f"📐 Размер: `{pizza_size}` (+{size_price} ⭐️)\n"
        f"🥤 Напиток: `{drink_name}` (+{drink_price} ⭐️)\n\n"
        f"💰 *Итого к оплате:* {total_stars} ⭐️\n\n"
        f"Пожалуйста, подтвердите ваш заказ:"
    )

    await message.edit_text(
        text=text, parse_mode="Markdown", reply_markup=get_wait_order_menu()
    )


@router.callback_query(OrderState.wait_for_drinks, DrinksCallback.filter())
async def wait_for_order_handler(
    callback: CallbackQuery, callback_data: DrinksCallback, state: FSMContext
) -> None:
    await state.update_data(drinks=callback_data.name)
    await state.set_state(OrderState.wait_for_order)
    await callback.answer()

    await show_order_confirmation_screen(callback.message, state)
