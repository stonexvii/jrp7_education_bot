from aiogram.fsm.state import State, StatesGroup


class GPTRequest(StatesGroup):
    wait_for_request = State()


class GPTTalk(StatesGroup):
    wait_for_answer = State()


class GPTQuiz(StatesGroup):
    wait_for_answer = State()
    wait_for_next_action = State()
