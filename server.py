import telebot
import config
from flask import Flask, app, request
from flask import send_from_directory

Token='8304724754:AAFW9hbOFNGCPI0vqQiN3OvTqz2IIwYQsVI'
client=telebot.TeleBot(config.config['token'])
webhook_path=f'/webhook{Token}'
app=Flask(__name__)

@app.route(webhook_path, methods={'POST'})
def webhook():
   update=telebot.types.Update.de_json(request.get_data().decode('utf-8'))
   client.process_new_updates([update])
   return 'ok', 200
@app.route('/local')
def get_rozklad():
    return send_from_directory(
        directory='local',
        path='zm.pdf')
 
if __name__=='__main__':
 app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)