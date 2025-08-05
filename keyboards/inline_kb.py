from aiogram.utils.keyboard import InlineKeyboardBuilder

from .callback_data import RandomGPT


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
