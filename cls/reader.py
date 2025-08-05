from aiogram.types import FSInputFile

import aiofiles


class Reader:

    def __init__(self, path: str):
        self._path = path

    async def load(self):
        if self._path.endswith('txt'):
            async with aiofiles.open(self._path, 'r', encoding='UTF-8') as file:
                response = await file.read()
                return response
        return FSInputFile(self._path)
