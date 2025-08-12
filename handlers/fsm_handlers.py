from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction

from .fsm_states import GPTRequest, GPTTalk
from keyboards.inline_kb import ikb_talk_back
from resources import resource
from cls import gpt_client
from cls.chat_gpt import ChatGPTMessage
from cls.enums import GPTRole

fsm_router = Router()


@fsm_router.message(GPTRequest.wait_for_request)
async def request_for_gpt(message: Message, bot: Bot, state: FSMContext):
    await bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING,
    )
    messages = ChatGPTMessage(resource.prompts['gpt'])
    messages.update(GPTRole.USER, message.text)
    response = await gpt_client.request(messages)
    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=resource.images['gpt'],
        caption=response,
    )
    await state.clear()


@fsm_router.message(GPTTalk.wait_for_answer)
async def question_for_celebrity(message: Message, bot: Bot, state: FSMContext):
    await bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING,
    )
    data = await state.get_data()
    if history_data := data.get('history', None):
        messages = history_data
    else:
        messages = ChatGPTMessage(resource.prompts[data['resource']])
    messages.update(GPTRole.USER, message.text)
    response = await gpt_client.request(messages)
    messages.update(GPTRole.CHAT, response)
    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=resource.images[data['resource']],
        caption=response,
        reply_markup=ikb_talk_back(),
    )
    await state.update_data({'history': messages})
