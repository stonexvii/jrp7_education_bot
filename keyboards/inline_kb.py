from aiogram.utils.keyboard import InlineKeyboardBuilder

from .callback_data import RandomGPT, TalkGPT
from resources import resource


def ikb_next_random():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text='Хочу еще факт',
        callback_data=RandomGPT(
            button='random',
            value='more',
        ),
    )
    keyboard.button(
        text='Хватит!',
        callback_data=RandomGPT(
            button='random',
            value='stop',
        ),
    )
    return keyboard.as_markup()


def ikb_talk_celebrity():
    keyboard = InlineKeyboardBuilder()
    buttons = resource.create_buttons()
    for file, text in buttons.items():
        keyboard.button(
            text=text,
            callback_data=TalkGPT(
                button='talk',
                file_name=file,
            ),
        )
    keyboard.button(
        text='Назад',
        callback_data=TalkGPT(
            button='back',
        )
    )
    keyboard.adjust(1)
    return keyboard.as_markup()


def ikb_talk_back():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text='Назад',
        callback_data=TalkGPT(
            button='back',
        )
    )
    return keyboard.as_markup()
