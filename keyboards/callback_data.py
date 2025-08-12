from aiogram.filters.callback_data import CallbackData


class RandomGPT(CallbackData, prefix='RG'):
    button: str
    value: str


class TalkGPT(CallbackData, prefix='TG'):
    button: str
    file_name: str = 'back'
