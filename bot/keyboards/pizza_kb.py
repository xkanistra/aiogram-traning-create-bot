from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class PizzaMenuCallback(CallbackData, prefix="pizza"):
    name: str


class PizzaSizeCallback(CallbackData, prefix="size"):
    name: str


def get_pizza_name_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Маргарита", callback_data=PizzaMenuCallback(name="margherita"))
    builder.button(text="Пепперони", callback_data=PizzaMenuCallback(name="pepperoni"))
    builder.button(
        text="Четыре сыра", callback_data=PizzaMenuCallback(name="quatro_stagioni")
    )
    builder.button(
        text="Капричоза", callback_data=PizzaMenuCallback(name="capricciosa")
    )
    builder.button(text="Дьявола", callback_data=PizzaMenuCallback(name="diavola"))
    builder.button(text="Прошутто", callback_data=PizzaMenuCallback(name="prosciutto"))

    # Размещаем inline клавиши по 2 в ряд
    builder.adjust(2)
    return builder.as_markup()


def get_pizza_size_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Маленькая (25см)", callback_data=PizzaMenuCallback(name="small")
    )
    builder.button(
        text="Средняя (30см)", callback_data=PizzaMenuCallback(name="medium")
    )
    builder.button(text="Большая (35см)", callback_data=PizzaMenuCallback(name="large"))
    builder.button(
        text="Очень большая (40см)", callback_data=PizzaMenuCallback(name="xl")
    )
    builder.button(
        text="⬅️ Назад", callback_data=PizzaMenuCallback(name="back_to_pizza_name")
    )

    # Размещаем inline клавиши размеров по 2 в ряд и назад отдельно
    builder.adjust(2, 2, 1)
    return builder.as_markup()
