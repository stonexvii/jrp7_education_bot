from .chat_gpt import ChatGPT
from .reader import Reader
from .resources import Resource

gpt_client = ChatGPT()

__all__ = [
    'gpt_client',
    'Reader',
    'Resource',
]
