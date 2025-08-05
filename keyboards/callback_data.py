from aiogram.filters.callback_data import CallbackData


class RandomGPT(CallbackData, prefix='RG'):
    button: str
    value: str
