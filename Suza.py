from apscheduler.schedulers.background import BackgroundScheduler
import telebot
import functionsSuza
from dotenv import load_dotenv
from Suza_game import *
from admin_func import *
from funy_func import *

# SV -1001721689921     Train -1001874349025 памятка для тестирования


load_dotenv()  # Загрузка значений из файла .env в переменные окружения
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)
states = ["Isbot?", "What_region?", "What_bike?", "What_birthday?"]

@bot.callback_query_handler(func=lambda callback: callback.data)
def take_callback(callback):
    if "newuser" in callback.data: # в колбеке еще слова с названием города
        register_new_user(bot, callback)
    elif "married" in callback.data:
        functionsSuza.Wedding(callback, bot)
    else:
        functionsSuza.suza_menu(callback, bot)


@bot.message_handler(func=lambda message: True,
                     content_types=[
                         'audio', 'photo','voice',
                         'video', 'video_note', 'document',
                         'text', 'location', 'contact', 'sticker'])
def take_message(message):
    # ведение статистики сообщений
    if message.chat.type == "supergroup":
        functionsSuza.Statistics(message)
    elif message.chat.type == "private":
        with sqlite3.connect("users.db") as con:
            cursor = con.cursor()
            cursor.execute(f"SELECT status FROM {message.chat.title} "
                           f"where user_id ==  {message.from_user.id}")
            result = cursor.fetchone()
            if result is None or result[0] != "Done":
                if result is None:
                    bot.reply_to(
                        message,
                        "Здравствуйте, не нашла вас "
                        "ни в одной из моих групп. "
                        "Видимо мы еще не знакомы? Тогда пожалуй вам "
                        "стоит начать с /help")
                        # проверить хелп сообщение
                elif result[0] != "Done":
                    keyb_new_user = types.InlineKeyboardMarkup(row_width=3)
                    btn_new_user = types.InlineKeyboardButton(
                        text="Начать заполнение анкеты.",
                        callback_data=f"newuser")
                    keyb_new_user.add(btn_new_user)
                    bot.reply_to(
                        message,
                        "Приветствую. У вас не заполнена анкета "
                        "для групповых чатов. "
                        "Давайте ее заполним", reply_markup =keyb_new_user)
    if message.text is not None:
        message.text = message.text.lower()
        if ("/help" in message.text
                or "суза" in message.text
                or "/start" in message.text
                or "/windbag" in message.text
                or "/holiday" in message.text
                or "/game" in message.text):
            functionsSuza.Help(message, bot)
        elif (message.text == "!stat"
              or message.text == "/!stat"
              or "/stat" in message.text):
            functionsSuza.StatConversations(message, bot)
        elif "!праздник" in message.text:
            hollidays(message,bot)
    if message.content_type == 'voice':
        functionsSuza.VoiceMsg(message, bot)
    if message.content_type == 'video_note':
        functionsSuza.VideoMsg(message, bot)
    if message.text is not None and "/menu" in message.text:
        functionsSuza.Menu(message, bot)

    game_words = [
        "спасибо", "погладить", "почесать спинку", "спс",
        "мой авторитет", "сяб", "пасибо", "пасяб", "поженимся",
        "чпок", "-", "+", "+++", "спиздить", "обчистить",
        "украсть", "обокрасть", "пнуть", "обнять", "обнимашки",
        "скрасть", "отпиздить", "опустить", "пнуть", "поцеловать",
        "поцелуй", "чмок", "целовашки", "подарить", "пожертвовать",
        "унизить", "зачмырить", "своровать", "затискать", "потискать"]
    if message.text in game_words and message.text is not None:
        play_process(message, bot)


@bot.message_handler(content_types=['new_chat_members'])
def admin(message):
     if message.chat.type == "supergroup":
        join_request(message, bot)

scheduler = BackgroundScheduler()
scheduler.add_job(
    functionsSuza.BirthdaySVClub, 'cron', hour=8, minute=0,
    timezone=pytz.timezone('Europe/Moscow'), args=[bot])
scheduler.add_job(
    kick_new_user, 'cron', hour=8, minute=0,
    timezone=pytz.timezone('Europe/Moscow'), args=[bot])
scheduler.add_job(
    functionsSuza.SaveStats, 'cron', hour=0, minute=0,
    timezone=pytz.timezone('Europe/Moscow'), args=['closeday'])
scheduler.add_job(
    functionsSuza.SaveStats, 'cron', day_of_week='mon',
    hour=0, minute=0, timezone=pytz.timezone('Europe/Moscow'),
    args=['closeweek'])
scheduler.add_job(
    functionsSuza.SaveStats, 'cron', day='1', hour=0, minute=0,
    timezone=pytz.timezone('Europe/Moscow'), args=['closemonth'])
scheduler.add_job(
    functionsSuza.SaveStats, 'cron', day='1', month='1',
    hour=0, minute=0,
    timezone=pytz.timezone('Europe/Moscow'), args=['NewYear'])
scheduler.start()

bot.infinity_polling()
