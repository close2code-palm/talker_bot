import random
import uuid
from aiogram.utils.i18n import gettext as _
# todo add markup

from aiogram.types import InlineQueryResultArticle, InputTextMessageContent


def polite_pls():
    return [_("Be so kind "), _("Please excuse me "), _("Would you be so kind "),
            _("Could you please "), _("We would appreciate it if you would ")]


def polite_thx():
    return [_("Thank you so much for everything."), _("Thank you very much for your support."),
            _("Thank you, that was very kind of you. "), _("I sincerely thank you."),
            _("I wouldn't have made it without you.")]


def polite_apl():
    return [_("Dear sir "), _("Dear Gentleman "), _("Dear Citizen ")]


def polite_greetings():
    return [_("I wish you a good day!"), _("Incredibly glad to see you!"),
            _("Greetings from the bottom of my heart!"), _("Hello, thanks for the contact!"), ]


def polite_goodbyes():
    return [_("Hope we meet again soon."), _("I was very happy to meet you!"),
            _("I would like our communication to remain as warm")]


def texts_polite():
    return [polite_goodbyes(), polite_greetings(), polite_apl(), polite_thx(), polite_pls()]


def menu_result():
    return [
        InlineQueryResultArticle(
            id=str(uuid.uuid4()), title=_('Eloquent pleases'), input_message_content=InputTextMessageContent(
                message_text=random.choice(polite_pls())
            )),
        InlineQueryResultArticle(id=str(uuid.uuid4()), title=_('Eloquent appeals'), input_message_content=InputTextMessageContent(
                message_text=random.choice(polite_apl())
            )),
        InlineQueryResultArticle(
            id=str(uuid.uuid4()), title=_('Eloquent goodbyes'), input_message_content=InputTextMessageContent(
                message_text=random.choice(polite_goodbyes())
            )),
        InlineQueryResultArticle(
            id=str(uuid.uuid4()), title=_('Eloquent gratitude'), input_message_content=InputTextMessageContent(
                message_text=random.choice(polite_thx())
            )
        ),
        InlineQueryResultArticle(id=str(uuid.uuid4()), title=_('Eloquent greetings'),
                                 input_message_content=InputTextMessageContent(
                                     message_text=random.choice(polite_greetings())
                                 )),
        InlineQueryResultArticle(id=str(uuid.uuid4()), title=_('Bot chat info'),
                                 input_message_content=InputTextMessageContent(
                                     message_text=_('💬 Bot chat appears here: @smart_abbot')
                                 ))
    ]
