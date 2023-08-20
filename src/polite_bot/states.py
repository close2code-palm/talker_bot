from aiogram.fsm.state import StatesGroup, State


class PhrasesSettings(StatesGroup):
    new_phrase_input = State()
    delete_phrase = State()
