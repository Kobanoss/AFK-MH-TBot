from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):
    question = State()
    wait = State()
    danger = State()
    selecting = State()
