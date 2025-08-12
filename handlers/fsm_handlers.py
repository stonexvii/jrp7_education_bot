from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction

from .fsm_states import GPTRequest, GPTTalk, GPTQuiz
from keyboards.inline_kb import ikb_talk_back, ikb_quiz_menu
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


@fsm_router.message(GPTQuiz.wait_for_answer)
async def quiz_answer(message: Message, state: FSMContext):
    user_answer = message.text
    data = await state.get_data()
    message_list = data['messages']
    message_list.update(GPTRole.USER, user_answer)
    response = await gpt_client.request(message_list)
    my_score = data['score'] + 1 if response == 'Правильно!' else data['score']
    message_list.update(GPTRole.CHAT, response)
    message_text = f'Ваш счет: {my_score}\n{response}'
    await message.answer(
        text=message_text,
        reply_markup=ikb_quiz_menu(),
    )
    await state.update_data({'score': my_score})
    await state.set_state(GPTQuiz.wait_for_next_action)
