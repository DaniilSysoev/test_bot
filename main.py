import telebot
from telebot import types
import time
import os
import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


delay = 0
chat_id = 0
flag = ""
token = "5751929492:AAF8mOvn_ZA8Cod3RoFZTcpFWz653XdGxWI"
bot = telebot.TeleBot(token)


def get_service_sacc():
    creds_json = os.path.dirname(__file__) + '/credentials.json'
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
    return build('sheets', 'v4', http=creds_service)


def get_data(name_sheet):
    service = get_service_sacc()
    sheet = service.spreadsheets()
    sheet_id = "1AKITTsmYIHwWoVH5jAzNIdRpsP7nZr6mKMzFIl2Z7bs"
    read = sheet.values().get(spreadsheetId=sheet_id, range=str(name_sheet)+"!A1:A").execute()
    return read

@bot.message_handler(commands=["start"])
def start(message):
    global delay
    global flag
    global chat_id
    bot.send_message(message.chat.id, "Введите время уведомлений")
    flag = "start"
    chat_id = message.chat.id


def send_message():
    global delay
    global chat_id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Видеоматериалы")
    btn2 = types.KeyboardButton("Дополнительные материалы")
    markup.add(btn1, btn2)
    bot.send_message(chat_id, "Выберите материалы", reply_markup=markup)
    while True:
        time.sleep(int(delay))
        bot.send_message(chat_id, "Вы хотите продолжить обучение?")


@bot.message_handler(content_types=["text"])
def main(message):
    global delay
    global flag
    global chat_id
    if flag == "start" and message.text.isdigit():
        delay = message.text
        send_message()
        flag = "main"
    else:
        data = get_data(message.text)
        text = [i for j in data["values"] for i in j]
        bot.send_message(chat_id, "\n".join(text))
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Видеоматериалы")
    btn2 = types.KeyboardButton("Дополнительные материалы")
    markup.add(btn1, btn2)
    bot.send_message(chat_id, "Выберите материалы", reply_markup=markup)


bot.polling(none_stop=True)