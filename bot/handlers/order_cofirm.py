# Хендлер принимает подтверждение заказа
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, LabeledPrice, Message, PreCheckoutQuery

from bot.infrastructure.storage_postgres import StoragePostgres
from bot.keyboards.pizza_kb import OrderCallback
from bot.states.order import OrderState

router = Router()


@router.callback_query(OrderState.wait_for_order, OrderCallback.filter(F.name == "pay"))
async def order_pay_handler(
    callback: CallbackQuery, callback_data: OrderCallback, state: FSMContext
) -> None:
    await callback.answer()

    data = await state.get_data()
    total_price = data.get("total_price", 0)
    pizza_name = data.get("pizza_name", "Не выбрана")
    pizza_size = data.get("pizza_size", "Не выбран")

    await state.set_state(OrderState.order_confirm)

    prices = [
        LabeledPrice(label=f"Пицца {pizza_name} {pizza_size}", amount=total_price)
    ]

    await callback.message.delete()

    await callback.message.answer_invoice(
        title="Оплата заказа пиццы",
        description=f"Оплата корзины на сумму {total_price} ⭐️",
        payload="stars_pizza_order_internal_payload",
        provider_token="",
        currency="XTR",
        prices=prices,
        start_parameter="pay",
    )


@router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery) -> None:
    # Здесь при необходимости можно сделать быстрый SELECT в пул asyncpg на проверку ингредиентов
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def successful_payment_handler(
    message: Message,
    state: FSMContext,
    storage: StoragePostgres,
) -> None:
    payment_info = message.successful_payment

    await storage.clear_user_state_and_order(message.from_user.id)

    await state.clear()

    await message.answer(
        text=(
            "🎉 *Большое спасибо за оплату!*\n\n"
            f"Списано: {payment_info.total_amount} ⭐️ (Telegram Stars).\n"
            "Ваш заказ успешно передан на кухню. Начинаем готовить! 🍕"
        ),
        parse_mode="Markdown",
    )
