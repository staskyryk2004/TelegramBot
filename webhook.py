import telebot
import config
Token='8304724754:AAFW9hbOFNGCPI0vqQiN3OvTqz2IIwYQsVI'
webhook_url=f'https://rozklad.cx.ua/webhook/{Token}'
client=telebot.TeleBot(config.config['token'])
client.remove_webhook()
client.set_webhook(url=webhook_url)