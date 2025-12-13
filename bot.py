import telebot
import config
from  telebot  import types
from io import BytesIO
from uuid import uuid4
import os
bot_token=os.environ.get('8304724754:AAFW9hbOFNGCPI0vqQiN3OvTqz2IIwYQsVI')
client=telebot.TeleBot(config.config['token'])

table_file='zm.pdf'
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
@client.message_handler(commands=['get_info','info'])
def get_user_info(message):
    markup_inline = types.InlineKeyboardMarkup()
    item_yes = types.InlineKeyboardButton(text='Так', callback_data='yes')
    item_no = types.InlineKeyboardButton(text='Ні', callback_data='no')
    markup_inline.add(item_yes,item_no)
    client.send_message(message.chat.id, 'Бажаєте дізнатися розклад',
        reply_markup=markup_inline)
    
@client.callback_query_handler(func=lambda call:True)
def answer(call):
    if call.data =='yes':
      markup_reply= types.ReplyKeyboardMarkup(resize_keyboard=True)
      item_tables=types.KeyboardButton('Розклад')
      markup_reply.add(item_tables)
      client.send_message(call.message.chat.id, 'Показати розклад:',
        reply_markup = markup_reply
        )
    elif call.data == 'no': 
       pass
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
