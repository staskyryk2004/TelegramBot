from flask import Flask, app, request
from email import message
import hashlib
from pydoc import text
import time
import io
import os
import pdfplumber
import re
import telebot
import config
import requests
from  telebot  import types 
from io import BytesIO
from uuid import uuid4
client=telebot.TeleBot(config.config['token'])
table_url='http://127.0.0.1:5000'
table_file="/home/ubuntu/TelegramBot/local/zm.pdf"
chat_id=6063647240
last_hash=None
@client.message_handler(commands=['start'])
def start(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Актуальний розклад','Команди сервера')
    client.send_message(message.chat.id, "Вітаю! Оберіть дію:",
        reply_markup=markup)
@client.message_handler(func=lambda m: m.text == 'Команди сервера')
def server_commands(message):
    text =('*Доступні команди бота:*\n\n'
        "▶ `/start` — запуск бота і показує меню команд які є на сервері\n"
        "▶ *Актуальний розклад* — завантажити PDF з сайту інституту\n"
        "▶ *Команди сервера* — показує список команд\n\n"
        "ℹ️ Бот працює на сервері\n"
        'ℹ️ Дані завантажуються безпосередньо з офіційного сайту')
    client.send_message(message.chat.id, text, parse_mode="Markdown")
@client.message_handler(commands=['help'])
def help_cmd(message):
   server_commands(message) 
@client.message_handler(func=lambda m: m.text == 'Актуальний розклад')
def send_table(message):
    client.send_message(message.chat.id,'Зачекайте завантажується актуальний розклад...')
    try:

        response=requests.get(f'{table_url}/local')
        file_bytes=BytesIO(response.content)
        file_bytes.name="zm.pdf"
        client.send_document(message.chat.id, file_bytes)

        text=''
        with pdfplumber.open(table_file) as pdf:
         for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + '\n'
            day=re.search(r'на\s+(понеділок|вівторок|середу|четвер|пʼятницю|суботу|неділю)', text, re.IGNORECASE)
            day=day.group(1) if day else 'Невідомо'
            date=re.search(r'\d{1,2}\s+(січня|лютого|березня|квітня|травня|червня|'
            r'липня|серпня|вересня|жовтня|листопада|грудня)\s+202\d', text)
            date=date.group(0) if date else 'Невідомо'
            client.send_message(message.chat.id,
                f'Актуальний розклад\n'
                f'День: {day}\n'
                f'Дата: {date}',
                parse_mode='Markdown')
        file_bytes.seek(0)
    except requests.exceptions.RequestException as e:
        client.send_message(message.chat.id, 
                f'Помилка завантаження розкладу:\n {e}')
    while True:
      response=requests.get(table_url)
      current_hash= hashlib.md5(response.content).hexdigest()
      time.sleep(0.1)
      if last_hash and current_hash != last_hash:
       client.send_message(chat_id, f'Дані оновлено') 
       client.send_message(chat_id, response.content) 
          
@client.message_handler(content_types=['document'])
def handle_docs_audio(message):
    content_type = message.content_type
    if content_type =='document':
        file_id=message.document.file_id
        file_name=message.document.file_name
        send=client.send_document
        file_info=client.get_file(file_id)
        downloaded=client.downloaded_file(file_info.file_path)
        file_bytes=BytesIO(downloaded)
        file_bytes.name= file_name
    send(
        chat_id=message.chat_id,
        data=file_bytes,
        caption=f"Файл отримано та виведено ботом\n {file_name}"
    )

@client.message_handler(commands=['id'])
def get_chat_id(message):
 client.send_message(message.chat.id, f'Показати id:{message.chat.id}',)
@client.message_handler(func=lambda m: m.text == 'Розклад',)
def send_table(message):
    with open(table_file, 'rb') as f:
        client.send_document(message.chat.id, f, caption='Актуальний розклад')
@client.message_handler(content_types = ['text'])
def get_text(message):
    if message.text.lower() == 'привіт':
        client.send_message(message.chat.id, 'Привіт, шановний користувачу')
@client.message_handler(content_types = ['text'])
def get_content(message):
    if message.text == 'Розклад':
        client.send_message(message.chat.id, f'Показати розклад: {message.from_item_tables}')
client.polling(none_stop = True, interval = 0)