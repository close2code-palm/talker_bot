from typing import Dict

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _

from src.polite_bot.cb_data import DeletePhrase, Languages


def phrases_action():
    pa_kbb = InlineKeyboardBuilder()
    pa_kbb.button(text=_('Show my templates'), callback_data='get_phrases')
    pa_kbb.button(text=_('Add template'), callback_data='add_phrase')
    pa_kbb.button(text=_('Delete a phrase'), callback_data='delete_phrase')
    pa_kbb.button(text=_('Change language'), callback_data='lang')
    pa_kbb.adjust(1, repeat=True)
    return pa_kbb.as_markup()


def languagues_kb(current_language: str):
    l_kbb = InlineKeyboardBuilder()
    langs_map = {
        'en': _('English'),
        'ru': _('Russian')
    }
    del langs_map[current_language]
    for k in langs_map:
        l_kbb.button(text=langs_map[k], callback_data=Languages(lang=k))
    return l_kbb.as_markup()


def delete_phrases_kb(phrases_with_ids: Dict[int, str]):
    delp_kbb = InlineKeyboardBuilder()
    for k in phrases_with_ids:
        delp_kbb.button(text=phrases_with_ids[k][:20], callback_data=DeletePhrase(
            phrase_id=k))
    delp_kbb.button(text=_('Stop deletion'), callback_data='cncl_del')
    delp_kbb.adjust(1, repeat=True)
    return delp_kbb.as_markup()
