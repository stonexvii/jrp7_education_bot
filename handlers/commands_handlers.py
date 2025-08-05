from aiogram import Bot, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext

from cls.chat_gpt import ChatGPT, ChatGPTMessage
from keyboards.reply_kb import kb_main_menu
from keyboards.inline_kb import ikb_next_random
from resources import resource
from .fsm_states import GPTRequest

command_router = Router()


@command_router.message(Command('start'))
async def com_start_handler(message: Message, bot: Bot):
    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=resource.images['main'],
        caption=resource.messages['main'],
        reply_markup=kb_main_menu(),
    )


@command_router.message(Command('random'))
async def random_handler(message: Message, bot: Bot):
    await bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING,
    )
    gpt_client = ChatGPT()
    message_list = ChatGPTMessage(resource.prompts['random'])
    response = await gpt_client.request(message_list)
    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=resource.images['random'],
        caption=response,
        reply_markup=ikb_next_random(),
    )


@command_router.message(Command('gpt'))
async def gpt_command(message: Message, bot: Bot, state: FSMContext):
    await state.set_state(GPTRequest.wait_for_request)
    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=resource.images['gpt'],
        caption=resource.messages['gpt'],
    )
