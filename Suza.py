import pickle
from apscheduler.schedulers.background import BackgroundScheduler
import telebot
import functionsSuza
from dotenv import load_dotenv
from Suza_game import *
from admin_func import *
from functionsSuza import *
from funy_func import *
from parts_article import  *
from telebot import *
from telebot import types

from test import save_testmessage


# SV -1001721689921     Train -1001874349025 памятка для тестирования
class ExceptionHandler:
    def handle(self, exception_info):
        print(f"Произошла ошибка: {exception_info}")

# Создаем экземпляр ExceptionHandler
exception_handler = ExceptionHandler()

load_dotenv()  # Загрузка значений из файла .env в переменные окружения
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN, exception_handler=exception_handler)


commands = ['/start', '/help', '/stat', '/kick', '/ban', '/mute']

game_words = [
        "спасибо","погладить", "почесать спинку", "спс","мой авторитет",
        "сяб", "пасибо", "пасяб", "спс", "поженимся", "чпок", "-", "+",
        "+++", "благодарю", "спиздить","обчистить", "украсть", "обокрасть",
        "пнуть", "обнять", "обнимашки", "скрасть", "отпиздить","опустить",
        "пнуть", "поцеловать", "поцелуй", "чмок", "целовашки", "подарить",
        "пожертвовать", "унизить", "зачмырить", "своровать","затискать",
        "потискать"
    ]

@bot.callback_query_handler(func=lambda callback: callback.data)
def take_callback(callback):
    if 'new_join_request' in callback.data and callback.from_user.id == int(callback.data.split()[1]):
        allow_request_new_member(callback.from_user.id, callback.message.chat.id, bot)

    elif "married" in callback.data:
        functionsSuza.Wedding(callback, bot)
    else:
        functionsSuza.suza_menu(callback, bot)

# загружаем сохраненное сообщение с нужными конфигурациями для тестов
# with open('mess.pickle', 'rb') as f:
#     saved_message = pickle.load(f)
@bot.message_handler(func=lambda message: True,
                     content_types=['text', 'animation', 'audio',
                                    'document', 'photo', 'sticker',
                                    'video', 'video_note', 'voice','new_chat_members'])
def take_message(message: Message):
    save_testmessage(message) #сохранение сообщения для тестов
    if message is not None and (message.chat.type == 'supergroup' or
            message.chat.type == 'private'):
        writing_statistics(message)
    if message.text is not None:
        for command in commands:
            if command in message.text.lower():
                check_command(message, bot)
        for word in game_words:
            if word in message.text.lower().split():
                play_process(message, bot, game_words)
    if message.content_type == 'new_chat_members' and message.chat.type == 'supergroup':
        join_request(message, bot)
    if message.content_type == 'voice' or message.content_type == 'vidoe_note':
        if message.content_type == 'voice':
            VoiceMsg(message, bot)
        elif message.content_type == 'video_note':
            VideoMsg(message, bot)


# вызываем нужную функцию и передаем загруженное сообщение для тестирования
#take_message(saved_message)


#     if message.text is not None:
#         message.text = message.text.lower()
#         if ("/help" in message.text
#                 or "суза" in message.text
#                 or "/start" in message.text
#                 or "/windbag" in message.text
#                 or "/holiday" in message.text
#                 or "/game" in message.text):
#             functionsSuza.Help(message, bot)
#         elif "!праздник" in message.text:
#             hollidays(message,bot)
#         elif "/parts" in message.text:
#             text = take_message_request(message)
#             bot.reply_to(
#                 message,
#                 text)
#     if message.text is not None and "/menu" in message.text:
#         functionsSuza.Menu(message, bot)
#
scheduler = BackgroundScheduler()
scheduler.add_job(kick_unverifed_user, 'interval', minutes=3, timezone=pytz.timezone('Europe/Moscow'), args=[bot])
# scheduler.add_job(
#     functionsSuza.BirthdaySVClub, 'cron', hour=8, minute=0,
#     timezone=pytz.timezone('Europe/Moscow'), args=[bot])
scheduler.start()

bot.infinity_polling()
