from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction

from .fsm_states import GPTRequest
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
