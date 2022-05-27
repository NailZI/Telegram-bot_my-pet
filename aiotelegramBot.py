# На 18.01.2022 последняя рабочая версия бота
# pip freeze > requirements.pip  # упаковка всех используемых библиотек
# pip install -r requirements.pip  # распаковка библиотек

import logging
import os
import re
import bot_conf  # файл в папке C:\...\bot_conf.py c настройками
import asyncio
import emoji

from contextlib import suppress
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import (MessageToEditNotFound, MessageCantBeEdited, MessageCantBeDeleted,
                                      MessageToDeleteNotFound)
from excel_read import find_text, find_id, find_kshm
from checkIP import responce_kshm

# Обьект бота
bot = Bot(token=bot_conf.master_token)  # API бота основного бота (Test_bot)
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

admin = bot_conf.admin  # Телеграм id администратора
folder = bot_conf.folder_test  # папка с программой
text_folder = bot_conf.text_folder_test  # папка с доп. материалами


def check_user(us_id):
    userID = us_id  # Извлекаем ID пользователя, приславшего сообщение
    os.chdir(folder)
    users = open('users.txt', 'r')  # Открываем список пользователей
    users_list = users.read()  # Читаем список
    if userID == admin:  # Если сообщение от администратора
        access = 1
    elif str(userID) in users_list:  # Если сообщение от зарегистрированного пользователя
        access = 2
    else:  # Если сообщение от незарегистрированного пользователя
        access = 0
    users.close()
    return access

# async def delete_message(message: types.Message, sleep_time: int = 0):
# Песочные часы включаются на время ожидания ответа от бота
# и исчезают по приходу ответа
async def delete_message(message: types.Message, flag: int = 1):  # функция песочных часов
    # await asyncio.sleep(sleep_time)
    if flag == 0:
        with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
            await message.delete()

# Создаем кнопку /help
@dp.message_handler(commands='')
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton(text="/help")
    keyboard.add(button)
    await message.answer("Нажмите кнопку /help", reply_markup=keyboard)

# выполнение команды /help
@dp.message_handler(commands='help')
async def cmd_answer(message: types.Message):
    user_ac = check_user(message.from_user.id)
    if user_ac != 0:  # если пользователь зарегистрирован
        #print(os.getcwd())
        os.chdir(text_folder)
        help_msg = open('help.md', 'r')
        resp_text = help_msg.read()
        help_msg.close()
        os.chdir('..')
        #print(os.getcwd())
    else:  # если нет
        resp_text = 'Вам необходимо пройти регистрацию, ' \
                    'для этого отправьте команду ' \
                    '/reg номер вашего телефона\n' \
                    'например:\n' \
                    '/reg 89191234567'
    await message.answer(resp_text) # parse_mode="MarkdownV2"

# выполнение команды /reg запрос на регистрацию от нового пользователя
@dp.message_handler(commands='reg')
async def cmd_answer(message: types.Message):
    await message.answer('Ждите сообщение о регистрации') # ответ запросившему
    telphn = re.findall(r'\d', message.text)
    tel_num = ''
    for i in range(len(telphn)): # вытаскиваем номер телефона из сообщения
        tel_num = tel_num + telphn[i]
    reg_mes = 'Пользователь ' + str(message.from_user.id) + \
              ' с номером телефона: ' + tel_num + \
              ' просит регистрацию'
    await message.bot.send_message(admin, reg_mes) # запрос админу

# выполнение команды /ping пингование IP адреса
@dp.message_handler(commands='ping')
async def cmd_answer(message: types.Message):
    user_ac = check_user(message.from_user.id)
    if user_ac != 0:
        msg = await message.answer(emoji.emojize(u"\u23F3"))
        asyncio.create_task(delete_message(msg, 1))
        resp_text = responce_kshm(message.from_user.id, 'ping', message.text)
        asyncio.create_task(delete_message(msg, 0))
    else:
        resp_text = 'Пользователь не зарегистрирован, нажмите /help'
    await message.answer(resp_text)

# выполнение команды /ps проверка на работу драйвера
@dp.message_handler(commands='ps')
async def cmd_answer(message: types.Message):
    user_ac = check_user(message.from_user.id)
    if user_ac != 0:
        msg = await message.answer(emoji.emojize(u"\u23F3"))
        asyncio.create_task(delete_message(msg, 1))
        resp_text = responce_kshm(message.from_user.id, 'ps', message.text)
        asyncio.create_task(delete_message(msg, 0))
    else:
        resp_text = 'Пользователь не зарегистрирован, нажмите /help'
    await message.answer(resp_text)

# выполнение команды /reboot перезагрузка КШ-М
@dp.message_handler(commands='reboot')
async def cmd_answer(message: types.Message):
    user_ac = check_user(message.from_user.id)
    if user_ac != 0:
        msg = await message.answer(emoji.emojize(u"\u23F3"))
        asyncio.create_task(delete_message(msg, 1))
        resp_text = responce_kshm(message.from_user.id, 'kill', message.text)
        asyncio.create_task(delete_message(msg, 0))
    else:
        resp_text = 'Пользователь не зарегистрирован, нажмите /help'
    await message.answer(resp_text)

# выполнение команды /log считывание лога
@dp.message_handler(commands='log')
async def cmd_answer(message: types.Message):
    user_ac = check_user(message.from_user.id)
    if user_ac != 0:
        msg = await message.answer(emoji.emojize(u"\u23F3"))
        asyncio.create_task(delete_message(msg, 1))
        resp_text = responce_kshm(message.from_user.id, 'log', message.text)
        asyncio.create_task(delete_message(msg, 0))
    else:
        resp_text = 'Пользователь не зарегистрирован, нажмите /help'
    if len(resp_text) > 4096:
        pos = 0
        step = 4096
        while step < len(resp_text):
            text = resp_text[pos:step]
            if resp_text[step - 1] == ' ':
                await message.answer(text)
                pos = step
                step += 4096
            else:
                step -= 1
        await message.answer(resp_text[step - 4096:])
    else:
        await message.answer(resp_text)

# поиск в журнале по тексту
@dp.message_handler(commands='find')
async def cmd_answer(message: types.Message):
    user_ac = check_user(message.from_user.id)
    if user_ac != 0:
        msg = await message.answer(emoji.emojize(u"\u23F3"))
        asyncio.create_task(delete_message(msg, 1))
        resp_text = find_text(message.from_user.id, message.text[6:])
        asyncio.create_task(delete_message(msg, 0))
    else:
        resp_text = 'Пользователь не зарегистрирован, нажмите /help'
    if len(resp_text)>4096:
        pos = 0
        step = 4096
        while step < len(resp_text):
            text = resp_text[pos:step]
            if resp_text[step-1] == ' ':
                await message.answer(text)
                pos = step
                step += 4096
            else:
                step -= 1
        await message.answer(resp_text[step-4096:])
    else:
        await message.answer(resp_text)

# поиск по номеру ID
@dp.message_handler(commands='id')
async def cmd_answer(message: types.Message):
    user_ac = check_user(message.from_user.id)
    if user_ac != 0:
        msg = await message.answer(emoji.emojize(u"\u23F3"))
        asyncio.create_task(delete_message(msg, 1))
        resp_text = find_id(message.from_user.id, message.text[3:])
        asyncio.create_task(delete_message(msg, 0))
    else:
        resp_text = 'Пользователь не зарегистрирован, нажмите /help'
    await message.answer(resp_text)

# поиск по номеру КШ(М)
@dp.message_handler(commands='kshm')
async def cmd_answer(message: types.Message):
    user_ac = check_user(message.from_user.id)
    if user_ac != 0:
        msg = await message.answer(emoji.emojize(u"\u23F3"))
        asyncio.create_task(delete_message(msg, 1))
        resp_text = find_kshm(message.from_user.id, message.text[6:])
        asyncio.create_task(delete_message(msg, 0))
    else:
        resp_text = 'Пользователь не зарегистрирован, нажмите /help'
    if len(resp_text) > 4096:
        pos = 0
        step = 4096
        while step < len(resp_text):
            text = resp_text[pos:step]
            if resp_text[step - 1] == ' ':
                await message.answer(text)
                pos = step
                step += 4096
            else:
                step -= 1
        await message.answer(resp_text[step - 4096:])
    else:
        await message.answer(resp_text)

# выполнение команды /add регистрация пользователя !!! только для админа!!!
@dp.message_handler(commands='add')
async def cmd_answer(message: types.Message):
    user_ac = check_user(message.from_user.id)
    if user_ac == 1:
        reg_id = re.findall(r'\d+', message.text)  # извлекаем ID пользователя из сообщения в виде списка
        reg_id = [int(i) for i in reg_id]  # приводим список к числу
        os.chdir(folder)
        user_reg = open('users.txt', 'a')  # Чтение списка пользователей
        user_reg.write(str(reg_id) + '\n')  # записываем данные пользователя
        user_reg.close()
        reg_mes = 'Пользователь с ID: ' + str(reg_id[0]) + ' зарегистрирован.'
        await message.answer(reg_mes)
        await message.bot.send_message(reg_id[0], 'Вы зарегистрированы.')

    else:
        resp_text = 'У вас нет прав на выполнение данной операции, нажмите /help'
        await message.answer(resp_text)

# если прислали просто сообщение
@dp.message_handler(content_types=['text'])
async def cmd_answer(message: types.Message):
    await message.answer('Я не понимаю тебя, напиши /help')

if __name__ == '__main__':
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
