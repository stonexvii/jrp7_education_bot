from aiogram.utils.keyboard import InlineKeyboardBuilder

from collections import namedtuple

from .callback_data import RandomGPT, TalkGPT, QuizGPT
from resources import resource

ButtonQuiz = namedtuple('ButtonQuiz', ['text', 'callback'])


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


def ikb_quiz_select():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        ButtonQuiz('Программирование', 'quiz_prog'),
        ButtonQuiz('Математика', 'quiz_math'),
        ButtonQuiz('Биология', 'quiz_biology'),
    ]
    for button in buttons:
        keyboard.button(
            text=button.text,
            callback_data=QuizGPT(
                button='quiz',
                subject=button.callback,
            ),
        )
    keyboard.adjust(1)
    return keyboard.as_markup()


def ikb_quiz_menu():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        ButtonQuiz('Ещё!', 'quiz_more'),
        ButtonQuiz('Сменить тему', 'change_subject'),
        ButtonQuiz('Закончить', 'stop'),
    ]
    for button in buttons:
        keyboard.button(
            text=button.text,
            callback_data=QuizGPT(
                button='next_quiz',
                subject=button.callback,
            ),
        )
    return keyboard.as_markup()
