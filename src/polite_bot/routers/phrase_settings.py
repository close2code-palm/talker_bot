from typing import Dict

from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _, FSMI18nMiddleware, I18n

from src.polite_bot.cb_data import DeletePhrase, Languages
from src.polite_bot.keyboards import phrases_action, delete_phrases_kb, languagues_kb
from src.polite_bot.services import Repository
from src.polite_bot.states import PhrasesSettings
from src.polite_bot.utils import reset_state_wo_locale

router = Router()


@router.message(Command('set'))
async def set_phrases(message: types.Message):
    await message.answer(_('What do you want to do?'), reply_markup=phrases_action())


@router.callback_query(F.data == 'get_phrases')
async def list_phrases(call: types.CallbackQuery, repo: Repository):
    phrases = await repo.get_phrases(str(call.from_user.id))
    answer_message = ''
    pc = 0
    for p in phrases:
        pc += 1
        answer_message += f'{pc}. {p}\n'
    await call.message.answer(answer_message)
    await call.answer()


@router.callback_query(F.data == 'add_phrase')
async def start_adding(call: types.CallbackQuery, state: FSMContext, repo: Repository):
    if await repo.limit_reached(str(call.from_user.id)):
        await call.message.answer(_('Limit reached.'))
    else:
        await state.set_state(PhrasesSettings.new_phrase_input)
        await call.message.answer(_('Please, enter new template text.'))
    await call.answer()


@router.message(PhrasesSettings.new_phrase_input)
async def save_phrase(message: types.Message, repo: Repository, state: FSMContext):
    await reset_state_wo_locale(state)
    await repo.save_phrase(str(message.from_user.id), message.text)
    await message.answer(_('Your new phrase saved.'))


@router.callback_query(F.data == 'lang')
async def change_lang(call: types.CallbackQuery, i18n: I18n):
    await call.message.answer(
        _('Choose a language'), reply_markup=languagues_kb(i18n.current_locale))
    await call.answer()


@router.callback_query(Languages.filter())
async def set_language(
        call: types.CallbackQuery,
        i18n_middleware: FSMI18nMiddleware,
        state: FSMContext,
        callback_data: Languages
):
    await i18n_middleware.set_locale(state, callback_data.lang)
    await call.message.answer(_('User inline search to refresh the cache.'))
    await call.answer()


@router.callback_query(F.data == 'delete_phrase')
async def delete_choice(call: types.CallbackQuery, state: FSMContext, repo: Repository):
    phrases = await repo.get_phrases(str(call.from_user.id))
    deletion_mapping = {i: v for i, v in enumerate(phrases)}
    await state.update_data(del_p=deletion_mapping)
    await state.set_state(PhrasesSettings.delete_phrase)
    await call.message.answer(
        _('Choose phrase to delete'),
        reply_markup=delete_phrases_kb(deletion_mapping)
    )
    await call.answer()


# todo check if we can add dict to state
@router.callback_query(DeletePhrase.filter(), PhrasesSettings.delete_phrase)
async def handle_deletion(
        call: types.CallbackQuery,
        repo: Repository,
        state: FSMContext,
        callback_data: DeletePhrase
):
    data = await state.get_data()
    await repo.remove_phrase(data['del_p'][callback_data.phrase_id])
    await call.message.answer(_('Deleted'))
    await call.answer()


@router.callback_query(F.data == 'cncl_del', PhrasesSettings.delete_phrase)
async def cancel_phrase_deletion_proc(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await reset_state_wo_locale(state)
    await call.answer()
