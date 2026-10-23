# Хендлер принимает отмену заказа
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.infrastructure.storage_postgres import StoragePostgres
from bot.keyboards.pizza_kb import OrderCallback, get_new_order_menu
from bot.states.order import OrderState

router = Router()


@router.callback_query(
    OrderState.wait_for_order, OrderCallback.filter(F.name == "cancel")
)
async def order_cancel_handler(
    callback: CallbackQuery,
    state: FSMContext,
    storage: StoragePostgres,
) -> None:
    await storage.clear_user_state_and_order(callback.from_user.id)
    await state.set_state(OrderState.order_cancel)
    await callback.message.edit_text(
        text="❌ Ваш заказ успешно отменен. Будем рады видеть вас снова!\nЧтобы сделать новый заказ, нажмите на кнопку ниже или введите команду /start.",
        reply_markup=get_new_order_menu(),
    )
