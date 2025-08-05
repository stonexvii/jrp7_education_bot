import openai

import config
from .enums import GPTRole


class ChatGPTMessage:

    def __init__(self, prompt: str):
        self._prompt = prompt
        self.message_list = self._init_message()

    def _init_message(self):
        message = {
            'role': GPTRole.SYSTEM.value,
            'content': self._prompt,
        }
        return [message]

    def update(self, role: GPTRole, message: str):
        self.message_list.append(
            {
                'role': role.value,
                'content': message,
            },
        )


class ChatGPT:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self._token = config.CHAT_GPT_TOKEN
        self._proxy = config.PROXY
        self._client = self._create_client()

    def _create_client(self):
        gpt_client = openai.AsyncOpenAI(
            api_key=self._token,
            base_url=self._proxy,
        )
        return gpt_client

    async def request(self, message: ChatGPTMessage, model: str = 'gpt-3.5-turbo'):
        response = await self._client.chat.completions.create(
            model=model,
            messages=message.message_list,
        )
        return response.choices[0].message.content
