from requests import post
from time import sleep
from datetime import datetime
import telebot
import json

f = open('settings.json', encoding='utf-8')
data = json.load(f)
f.close()

USE_TG_BOT = (data["telegram_bot_token"] != "" and data["telegram_bot_token"] != "None" and data["telegram_bot_token"] != "null"
              and data["tg_user_id"] != "" and data["tg_user_id"] != "None" and data["tg_user_id"] != "null")

if USE_TG_BOT:
    bot = telebot.TeleBot(token=data["telegram_bot_token"])
    TG_USER_ID = data["tg_user_id"]

def logToFile(message):
    if str(message) == "":
        return

    filename = "log_" + str(datetime.now().month) + "_" + str(datetime.now().year) + '.txt'

    open("Logs\\" + filename, 'a', encoding='utf-8').close()

    file = open("Logs\\" + filename, 'r+', encoding='utf-8')
    content = file.read()  # Чтение
    file.seek(0, 0)  # Переход в начало файла
    file.write(str(datetime.now()) + " | " + str(message) + "\n")
    file.write(content)
    file.close()

def log(message, username=None):
    if username is not None:
        message = "| юзер: " + username + " | " + message

    logToFile(message)

    f = open('settings.json', encoding='utf-8')
    data = json.load(f)
    f.close()

    if USE_TG_BOT and data["tg_notify_only_on_errors"] == "False":
        bot.send_message(chat_id=TG_USER_ID, text=message)

def logError(message, username=None):
    if username is not None:
        message = "| юзер: " + username + " | " + message

    logToFile(message)

    if USE_TG_BOT:
        bot.send_message(chat_id=TG_USER_ID, text=message)

def update_resume():
    f = open('settings.json', encoding='utf-8')
    data = json.load(f)
    f.close()

    for user in data["users"]:
        for resume in user["resumes_ids"]:
            headers = {'Authorization': f'Bearer {user["access_token"]}'}
            response = post( f'https://api.hh.ru/resumes/{resume}/publish/', headers=headers)

            if response.status_code == 204:
                log('Резюме успешно обновлено!', user["name"])
                continue
            elif response.status_code == 429:
                log('Резюме пока нельзя обновить', user["name"])
                continue

            error_code = response.status_code
            error_value = response.json()['errors'][0]['value']

            if error_value == 'token_expired':
                refresh_token(user)
                continue

            logError(f'Ошибка {error_code}: {error_value}', user["name"])

def refresh_token(user):
    headers = {'Authorization': f'Bearer {user["access_token"]}'}
    body = {'grant_type': 'refresh_token', 'refresh_token': user["refresh_token"]}
    response = post(f'https://hh.ru/oauth/token/', headers=headers, data=body)

    if response.status_code == 200:
        new_access_token = response.json()['access_token']
        new_refresh_token = response.json()['refresh_token']
        replace_tokens(user, new_access_token, new_refresh_token)
        log('Токен успешно обновлён!', user["name"])
        update_resume()

    error_code = response.status_code
    error = response.json()['error']
    error_description = response.json()['error_description']
    logError(f'Ошибка {error_code}. {error}: {error_description}', user["name"])

def replace_tokens(user, new_access_token, new_refresh_token):
    f = open('settings.json', encoding='utf-8')
    data = f.read()
    f.close()

    data = str(data).replace(user["access_token"], new_access_token)
    data = str(data).replace(user["refresh_token"], new_refresh_token)

    file = open('settings.json', 'w', encoding='utf-8')
    file.write(data)
    file.close()

if __name__ == '__main__':
    log('Начал работу!')

    while True:
        try:
            update_resume()
            sleep(4 * 60 * 60 + 10)
        except:
            sleep(10)