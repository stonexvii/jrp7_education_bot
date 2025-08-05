import dotenv
import os

dotenv.load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_GPT_TOKEN = os.getenv('CHAT_GPT_TOKEN')
PROXY = os.getenv('PROXY')
