from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class PizzaMenuCallback(CallbackData, prefix="pizza"):
    name: str


class PizzaSizeCallback(CallbackData, prefix="size"):
    name: str


class DrinksCallback(CallbackData, prefix="drink"):
    name: str


class OrderCallback(CallbackData, prefix="order"):
    name: str


class CancelOrderCallback(CallbackData, prefix="new"):
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
        text="Маленькая (25см)", callback_data=PizzaSizeCallback(name="small")
    )
    builder.button(
        text="Средняя (30см)", callback_data=PizzaSizeCallback(name="medium")
    )
    builder.button(text="Большая (35см)", callback_data=PizzaSizeCallback(name="large"))
    builder.button(
        text="Очень большая (40см)", callback_data=PizzaSizeCallback(name="xl")
    )
    builder.button(
        text="⬅️ Назад", callback_data=PizzaSizeCallback(name="back_to_pizza_name")
    )

    # Размещаем inline клавиши размеров по 2 в ряд и назад отдельно
    builder.adjust(2, 2, 1)
    return builder.as_markup()


def get_drinks_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Coca-Cola", callback_data=DrinksCallback(name="coca_cola"))
    builder.button(text="Fanta", callback_data=DrinksCallback(name="fanta"))
    builder.button(text="Pepsi", callback_data=DrinksCallback(name="pepsi"))
    builder.button(text="7-Up", callback_data=DrinksCallback(name="7-up"))
    builder.button(text="Вода", callback_data=DrinksCallback(name="water"))
    builder.button(text="Без напитка", callback_data=DrinksCallback(name="none"))
    builder.button(
        text="⬅️ Назад", callback_data=DrinksCallback(name="back_to_pizza_size")
    )

    builder.adjust(2, 2, 2, 1)
    return builder.as_markup()


def get_wait_order_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="✅Все верно, заказываю.", callback_data=OrderCallback(name="confirm")
    )
    builder.button(text="❌Отменить заказ.", callback_data=OrderCallback(name="cancel"))
    builder.button(text="⬅️ Назад", callback_data=OrderCallback(name="back_to_drinks"))

    builder.adjust(2, 1)
    return builder.as_markup()


def get_new_order_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Сделать новый заказ.", callback_data=CancelOrderCallback(name="order")
    )

    builder.adjust(1)
    return builder.as_markup()
