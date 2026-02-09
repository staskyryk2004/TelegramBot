from flask import Flask, app, request
from flask import send_from_directory
import telebot
import config
client=telebot.TeleBot(config.config['token'])
app=Flask(__name__)
@app.route('/local')
def get_rozklad():
    return send_from_directory(
        directory='local',
        path='zm.pdf')
if __name__=='__main__':
 app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)