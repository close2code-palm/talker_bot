import asyncio
from contextlib import suppress

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommand
from aiogram.utils.i18n import I18n, FSMI18nMiddleware, ConstI18nMiddleware, SimpleI18nMiddleware
from redis.asyncio import ConnectionPool, Redis

from src.polite_bot.middleware import DatabaseMiddleware
from src.polite_bot.routers import inline_templates, phrase_settings
from src.polite_bot.config import read_config


async def main():
    config = read_config('config.ini')
    pool = ConnectionPool(host=config.redis.host, db=config.redis.db_name)
    storage_con = Redis(connection_pool=pool)
    storage = RedisStorage(storage_con)
    dispatcher = Dispatcher(storage=storage)

    i18n = I18n(path="locales", default_locale="en", domain="messages")
    i18n_mw = FSMI18nMiddleware(i18n)
    i18n_mw.setup(dispatcher)

    db_mw = DatabaseMiddleware(pool)
    dispatcher.callback_query.outer_middleware(db_mw)
    dispatcher.message.outer_middleware(db_mw)
    dispatcher.inline_query.outer_middleware(db_mw)

    dispatcher.include_router(inline_templates.router)
    dispatcher.include_router(phrase_settings.router)
    bot = Bot(config.telegram.token)
    await bot.set_my_commands([
        BotCommand(command='set', description='Phrase and language management')
    ])
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    with suppress(KeyboardInterrupt):
        asyncio.run(main())

