from enum import Enum


class GPTRole(Enum):
    USER = 'user'
    CHAT = 'assistant'
    SYSTEM = 'system'
