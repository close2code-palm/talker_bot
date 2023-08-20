from aiogram.filters.callback_data import CallbackData


class DeletePhrase(CallbackData, prefix='del_p'):
    phrase_id: int


class Languages(CallbackData, prefix='langs'):
    lang: str
