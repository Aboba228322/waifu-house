from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text

async def settings_handler(message: types.Message):
    response_text = "Настройки:\n1. Выбор промтов\n2. Изменение языка\n3. Сброс настроек"
    await message.reply(response_text)

def register_handlers_settings(dp: Dispatcher):
    dp.register_message_handler(settings_handler, Text(equals="⚙️Настройки", ignore_case=True))
