import telebot
from telebot import types
from telebot.types import *
import sqlite3
import  re


path = "Suzuki.db"
def take_message_request(message:Message):
    years = list(range(1999, 2018))
    capacity = ""
    year_bike = ""
    partnumber = ""
    text = ""
    if "650s" in message.text.lower() or "650 s" in message.text.lower():
        capacity += "650 S"
    elif "650" in message.text.lower():
        capacity += "650"
    for el in years:
        if str(el) in message.text:
            year_bike += str(el)
    if "артикул" in message.text.lower() or "номер" in message.text.lower() or "партномер" in message.text.lower():
        pattern = r"\b\d{5}-\w{3,5}-\w{3}\b"
        match = re.search(pattern, message.text.lower())
        if match:
            partnumber = match.group()
        else:
            partnumber = ""
    if capacity == "" or year_bike == "":
        text += searching_part_and_bike([capacity, year_bike, partnumber])
    elif partnumber == "" and capacity != "" and year_bike != "":
        text += searching_model([capacity, year_bike, partnumber])
    return  text

def searching_part_and_bike(search_list):
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    query = """
    SELECT model, part FROM models
    WHERE partnumber LIKE ?
    """
    cursor.execute(query, (f"%{search_list[2]}%",))
    results = list(set(cursor.fetchall()))
    connection.close()
    if results:
        text_to_send = ""
        for result in results:
            text = f"Модель мотоцикла - {result[0]},\n узел/запчасть - {result[1]}\n\n"
            text_to_send += text
        # result = list(set([str(row[0]) + " " + row[1] + " " + row[2] for row in results]))
        # text = " \n".join(result)
        print(result)
        return text_to_send
    else:
        print("Совпадений не найдено.")

def searching_model(search_list):
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    query = """
        SELECT model FROM models
        WHERE model LIKE ? AND model LIKE ?
        """
    cursor.execute(query, (f"%{search_list[0]}%", f"%{search_list[1]}%"))
    results = list(set(cursor.fetchall()))
    connection.close()
    if results:
        text_to_send = ""
        for result in results:
            text = f"Модель мотоцикла - {result[0]},\n"
            text_to_send += text
        return  text_to_send
    else:
        return "Нет совпадений"