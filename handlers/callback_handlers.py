from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.enums import ChatAction

from cls.chat_gpt import ChatGPT, ChatGPTMessage
from resources import resource
from keyboards.inline_kb import ikb_next_random
from keyboards.callback_data import RandomGPT

callback_router = Router()


@callback_router.callback_query(RandomGPT.value == 'stop')
async def stop_random(callback: CallbackQuery, bot: Bot):
    await bot.edit_message_media(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(
            media=resource.images['main'],
            caption=resource.messages['main'],
        ),
    )


@callback_router.callback_query(RandomGPT.value == 'more')
async def one_more_random(callback: CallbackQuery, bot: Bot):
    await bot.send_chat_action(
        chat_id=callback.from_user.id,
        action=ChatAction.TYPING,
    )
    gpt_client = ChatGPT()
    message_list = ChatGPTMessage(resource.prompts['random'])
    response = await gpt_client.request(message_list)
    await bot.edit_message_media(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(
            media=resource.images['random'],
            caption=response),
        reply_markup=ikb_next_random(),
    )
