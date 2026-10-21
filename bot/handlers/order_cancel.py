# Хендлер принимает отмену заказа
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.keyboards.pizza_kb import OrderCallback, get_new_order_menu
from bot.states.order import OrderState

router = Router()


@router.callback_query(OrderState.wait_for_order, OrderCallback.filter())
async def order_cancel_handler(
    callback: CallbackQuery, callback_data: OrderCallback, state: FSMContext
) -> None:
    await state.clear()
    await state.set_state(OrderState.order_cancel)
    await callback.message.edit_text(
        text="❌ Ваш заказ успешно отменен. Будем рады видеть вас снова!\nЧтобы сделать новый заказ, нажмите на кнопку ниже или введите команду /start.",
        reply_markup=get_new_order_menu(),
    )
