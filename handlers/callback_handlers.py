from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext

from cls import gpt_client
from cls.chat_gpt import ChatGPT, ChatGPTMessage
from cls.enums import GPTRole
from resources import resource
from keyboards.inline_kb import ikb_next_random, ikb_quiz_select
from keyboards.callback_data import RandomGPT, TalkGPT, QuizGPT
from .fsm_states import GPTTalk, GPTQuiz

callback_router = Router()


@callback_router.callback_query(QuizGPT.filter(F.subject == 'stop'))
@callback_router.callback_query(TalkGPT.filter(F.button == 'back'))
@callback_router.callback_query(RandomGPT.filter(F.value == 'stop'))
async def stop_random(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.edit_message_media(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(
            media=resource.images['main'],
            caption=resource.messages['main'],
        ),
    )
    data = await state.get_data()
    score = data.get('score', None)
    if score is not None:
        await callback.answer(
            text=f'Ваш счет {score}!',
            show_alert=True,
        )
    await state.clear()


@callback_router.callback_query(RandomGPT.filter(F.value == 'more'))
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


@callback_router.callback_query(TalkGPT.filter(F.button == 'talk'))
async def select_celebrity(callback: CallbackQuery, callback_data: TalkGPT, bot: Bot, state: FSMContext):
    await bot.edit_message_media(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(
            media=resource.images[callback_data.file_name],
            caption='Задай свой первый вопрос: ',
        )
    )
    await state.set_state(GPTTalk.wait_for_answer)
    await state.set_data({'resource': callback_data.file_name})


@callback_router.callback_query(QuizGPT.filter(F.subject == 'change_subject'), GPTQuiz.wait_for_next_action)
async def quiz_change_subject(callback: CallbackQuery, callback_data: QuizGPT, bot: Bot, state: FSMContext):
    await bot.send_photo(
        chat_id=callback.from_user.id,
        photo=resource.images['quiz'],
        caption=resource.messages['quiz'],
        reply_markup=ikb_quiz_select(),
    )


@callback_router.callback_query(QuizGPT.filter(F.subject == 'quiz_more'))
@callback_router.callback_query(QuizGPT.filter(F.button == 'quiz'))
async def quiz_answer(callback: CallbackQuery, callback_data: QuizGPT, bot: Bot, state: FSMContext):
    await bot.send_chat_action(
        chat_id=callback.from_user.id,
        action=ChatAction.TYPING,
    )
    data = await state.get_data()
    if not data:
        messages_list = ChatGPTMessage(resource.prompts['quiz'])
        await state.set_data(
            {
                'messages': messages_list,
                'score': 0,
            }
        )
    else:
        messages_list: ChatGPTMessage = data['messages']
    messages_list.update(GPTRole.USER, callback_data.subject)
    response = await gpt_client.request(messages_list)
    messages_list.update(GPTRole.CHAT, response)
    await bot.edit_message_media(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(
            media=resource.images['quiz'],
            caption=response,
        )
    )
    await state.set_state(GPTQuiz.wait_for_answer)
    await state.update_data({'messages': messages_list})
