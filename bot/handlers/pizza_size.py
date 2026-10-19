# Хендлер обрабатывает нажатие выбора пиццы
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.keyboards.pizza_kb import PizzaMenuCallback, get_pizza_size_menu

# from bot.infrastructure.storage_postgres import StoragePostgres
from bot.states.order import OrderState

# Создаем роутер для файла
router = Router()


@router.callback_query(OrderState.wait_for_pizza_name, PizzaMenuCallback.filter())
async def pizza_size_handler(
    callback: CallbackQuery, callback_data: PizzaMenuCallback, state: FSMContext
) -> None:
    name_mapping = {
        "margherita": "Маргарита",
        "pepperoni": "Пепперони",
        "quatro_stagioni": "Четыре сыра",
        "capricciosa": "Капричоза",
        "diavola": "Дьявола",
        "prosciutto": "Прошутто",
    }

    pizza_name = name_mapping.get(callback_data.name, "Не выбрана")

    await state.update_data(pizza_name=pizza_name)
    await state.set_state(OrderState.wait_for_pizza_size)

    await callback.answer()

    await callback.message.edit_text(
        text=f"🍕Пицца: {pizza_name} \n📐Выберите размер пиццы:",
        reply_markup=get_pizza_size_menu(),
    )
