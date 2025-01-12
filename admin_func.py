import time

from telebot import types
import sqlite3
import datetime

def join_request(message, bot):
    current_time = int((datetime.datetime.now() + datetime.timedelta(minutes=3)).timestamp())
    bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=current_time, can_send_messages=False, can_send_media_messages=False, can_send_polls=False, can_send_other_messages=False, can_add_web_page_previews=False, can_change_info=False, can_invite_users=False, can_pin_messages=False)
    with sqlite3.connect("users.db") as con:
        cursor = con.cursor()
        cursor.execute(f"SELECT status FROM {message.chat.title} where user_id ==  {message.from_user.id}")
        result = cursor.fetchone()
        if result is None or result[0] != "Done":
            #keyb_new_user = types.InlineKeyboardMarkup(row_width=3)
            #btn_new_user = types.InlineKeyboardButton(text="Жми, если не бот.", callback_data=f"newuser?")
            #keyb_new_user.add(btn_new_user)
            cursor.execute(f"INSERT OR REPLACE INTO {message.chat.title} (user_id, username, lastname, firstname, daystats, weekstats, monthstats, yearstats, status) VALUES ({message.from_user.id}, '{message.from_user.username}', '{message.from_user.last_name}', '{message.from_user.first_name}', 0, 0, 0, 0, 'new_user {current_time}')")
            con.commit()
            bot.reply_to(message, "Если ты не бот, и хочешь быть участником этой группы - напиши мне в личку и пройди анкетирование в течении 3 минут.")
        elif result[0] == "Done":
            bot.reply_to(message, "С возвращением!")
            cursor.execute(f"INSERT OR REPLACE INTO {message.chat.title} (username, lastname, firstname) VALUES ('{message.from_user.username}', '{message.from_user.last_name}', '{message.from_user.first_name}')")
            bot.restrict_chat_member(message.chat.id, message.from_user.id,  can_send_messages=True, can_send_media_messages=True, can_send_polls=True, can_send_other_messages=True, can_add_web_page_previews=True, can_change_info=True, can_invite_users=True, can_pin_messages=True)

def register_new_user(bot, callback):
    with sqlite3.connect("users.db") as con:
        cursor = con.cursor()
        if callback.data == "newuser":
            keyboard = types.InlineKeyboardMarkup()
            buttons = [types.InlineKeyboardButton(city, callback_data="newuser What_region? " + city.lower()) for city in ['Москва', 'Спб', 'Тверь', 'Новгород']]
            keyboard.add(*buttons)
            cursor.execute(f"UPDATE {callback.message.chat.title} SET state = 'What_region?'  WHERE user_id = {callback.message.from_user.id}")
            bot.reply_to(callback.message, "Из какой ты области?", reply_markup = keyboard)
            con.commit()
        elif "newuser What_region?" in callback.data:
            keyboard = types.InlineKeyboardMarkup()
            buttons = [types.InlineKeyboardButton(bike, callback_data="newuser What_bike? " + bike.lower()) for bike in ['SV400', 'SV650', 'SV1000', 'SFV']]
            keyboard.add(*buttons)
            cursor.execute(f"UPDATE {callback.message.chat.title} SET state = 'What_bike?' WHERE user_id = {callback.message.from_user.id}")
            bot.reply_to(callback.message, "Какой у тебя байк??", reply_markup=keyboard)
            con.commit()
        elif "newuser What_bike?" in callback.data:
            keyboard = types.InlineKeyboardMarkup()
            buttons = [types.InlineKeyboardButton(birthday, callback_data="newuser What_birthday? " + birthday) for birthday in range(1,32)]
            keyboard.add(*buttons)
            cursor.execute(f"UPDATE {callback.message.chat.title} SET state = 'What_birthday?' WHERE user_id = {callback.message.from_user.id}")
            bot.reply_to(callback.message, "Какого числа ты родился?", reply_markup=keyboard)
            con.commit()
        elif callback.data == "newuser What_birthday?":
            keyboard = types.InlineKeyboardMarkup()
            buttons = [types.InlineKeyboardButton(birthday, callback_data="newuser What_birthday? " + birthday) for birthday in range(1,13)]
            keyboard.add(*buttons)
            cursor.execute(f"UPDATE {callback.message.chat.title} SET state = 'Done?' WHERE user_id = {callback.message.from_user.id}")
            con.commit()




def check_new_user(message, msg):
    with sqlite3.connect("users.db") as con:
        name_table = "statsmsg" + str(abs(message.chat.id))
        cursor = con.cursor()
        cursor.execute(f"SELECT * FROM {name_table} WHERE user_id == {message.from_user.id}")
        result = cursor.fetchone()
        if result is None:
            cursor.execute(f"INSERT INTO {name_table} (user_id, username, lastname, firstname, daystats, weekstats, monthstats, yearstats, mute) VALUES ({message.from_user.id}, '{message.from_user.username}', '{message.from_user.last_name}', '{message.from_user.first_name}', 0, 0, 0, 0, 'True {msg.chat.id} {msg.id}')")
            con.commit()
        else:
            cursor.execute(f"UPDATE {name_table} SET username = '{message.from_user.username}', lastname = '{message.from_user.last_name}', firstname = '{message.from_user.first_name}', mute = 'True {msg.chat.id} {msg.id}' WHERE user_id = {message.from_user.id}")
            con.commit()


def kick_new_user(bot):
    with sqlite3.connect("users.db") as con:
        cursor = con.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'statsmsg%'")
        tables = cursor.fetchall()
        for table in tables:
            cursor.execute(f"SELECT * FROM {table[0]} WHERE mute LIKE 'True%'")
            result = cursor.fetchall()
            for res in result:
                res_msg = res[8].split()
                if res_msg[0] == "True":
                    chat_id = "-" + table[0][8:]
                    user_id = res[0]
                    bot.unban_chat_member(chat_id,user_id)
                    bot.delete_message(res_msg[1],res_msg[2])
                    cursor.execute(f"DELETE FROM {table[0]} WHERE user_id = {user_id}")
                    con.commit()
                    bot.send_message(chat_id, "Ой, кажется кто-то вылетел из чата...\n(не люблю конкурентов\U0001F608)")

def allow_request(bot, callback):
    callback.data = int(callback.data.split()[1])
    if callback.from_user.id != callback.data:
        bot.send_message(callback.message.chat.id, "Это не тебе")
    else:
        bot.restrict_chat_member(callback.message.chat.id, callback.from_user.id, can_send_messages=True, can_send_media_messages = True, can_send_polls = True, can_send_other_messages = True, can_add_web_page_previews = True, can_change_info = False, can_invite_users = True, can_pin_messages = False)
        with sqlite3.connect("users.db") as con:
            name_table = "statsmsg" + str(abs(callback.message.chat.id))
            cursor = con.cursor()
            cursor.execute(f"SELECT mute FROM {name_table} WHERE user_id = {callback.from_user.id}")
            result = list(cursor.fetchone())
            res_msg = result[0].split()
            bot.delete_message(res_msg[1],res_msg[2])
            cursor.execute(f"UPDATE {name_table} SET username = '{callback.from_user.username}', lastname = '{callback.from_user.last_name}', firstname = '{callback.from_user.first_name}', mute = 'False' WHERE user_id = {callback.from_user.id}")
            con.commit()
