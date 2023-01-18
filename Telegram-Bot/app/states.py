from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):
    question = State()
    wait = State()
    selecting = State()
