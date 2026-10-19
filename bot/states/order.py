from aiogram.fsm.state import State, StatesGroup


class OrderState(StatesGroup):
    wait_for_pizza_name = State()
    wait_for_pizza_size = State()
    wait_for_drinks = State()
    wait_for_order = State()
    order_confirm = State()
    order_cancel = State()
    order_finished = State()
