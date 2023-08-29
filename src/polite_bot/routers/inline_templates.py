import uuid

from aiogram import Router, types
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent

from src.polite_bot.services import Repository
from src.polite_bot.texts import texts_polite, menu_result

router = Router()


@router.inline_query()
async def handle_inline_call(inline: types.InlineQuery, repo: Repository):
    search_results = []
    all_texts = []
    all_texts.extend(texts_polite())
    all_texts.extend(await repo.get_phrases(str(inline.from_user.id)))
    for text_set in all_texts:
        for text in text_set:
            if inline.query in text:
                search_results.append(text)

    if inline.query == '' or not search_results:
        return await inline.answer(menu_result())
    inline_result = [InlineQueryResultArticle(
        id=str(uuid.uuid4()), title=text_found,
        input_message_content=InputTextMessageContent(message_text=text_found))
        for text_found in search_results]
    await inline.answer(inline_result)
