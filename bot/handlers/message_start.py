# Хендлер отправляет сообщ при входе пользователя
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.infrastructure.storage_postgres import StoragePostgres
from bot.keyboards.pizza_kb import CancelOrderCallback, get_pizza_name_menu
from bot.states.order import OrderState

# Создаем роутер для файла
router = Router()


@router.message(CommandStart())
async def command_start(
    message: Message, state: FSMContext, storage: StoragePostgres
) -> None:
    # Очищаем состояние пользователя
    await state.clear()
    await state.set_state(OrderState.wait_for_pizza_name)
    await message.answer(
        f"Привет {message.from_user.first_name}! \n"
        f"🍕Добро пожаловать в пиццерию! Выберите пиццу из меню ниже:",
        reply_markup=get_pizza_name_menu(),
    )


@router.callback_query(OrderState.order_cancel, CancelOrderCallback.filter())
async def callback_new_order(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()

    # Узнаем в каком состоянии заказ клиента
    current_state = await state.get_state()

    # Очищаем старое состояние клиента
    await state.clear()
    await state.set_state(OrderState.wait_for_pizza_name)

    if current_state == OrderState.order_confirm.state:
        await callback.message.delete()
        await callback.message.answer(
            "🍕Пожалуйста выберите пиццу из меню ниже:",
            reply_markup=get_pizza_name_menu(),
        )
    else:
        await callback.message.edit_text(
            "🍕Пожалуйста выберите пиццу из меню ниже:",
            reply_markup=get_pizza_name_menu(),
        )
