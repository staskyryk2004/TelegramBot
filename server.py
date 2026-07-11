from flask import Flask, app, request
from flask import send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import telebot
import config
client=telebot.TeleBot(config.config['token'])
app=Flask(__name__)
limiter=Limiter(
    get_remote_address,
    app=app,
    storage_uri="memory://")

@app.route('/')
def home():
    return "Сервер працює стабільно!", 200
@app.route('/local')
@limiter.limit("10 per minute", "20 per hour")
def get_rozklad():
    return send_from_directory(
        directory='local',
        path='zm.pdf')
if __name__=='__main__':
 app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)