from utils import CsesClient
from pymongo import MongoClient
from db import Db
import time
from dotenv import load_dotenv
import telebot
import os
import random

load_dotenv()

try:
    cses_client = CsesClient(os.getenv("CSES_USERNAME"), os.getenv("CSES_PASSWORD"))
except Exception as e:
    print(f"[FATAL] Could not create CsesClient: {e}")
    exit(1)

db = Db(cses_client, "users")




#db.add_user("Ezegor", 192852)

cses_ids = [192852,252177, 252209, 345370, 283319, 345367, 252191]

def check_for_solved_task(cses_id):
    old_tasks = db.get_user_tasks(cses_id)
    cur_tasks = cses_client.get_user_tasks(cses_id)

    old_dict = {task['id']: task for task in old_tasks}
    cur_dict = {task['id']: task for task in cur_tasks}

    task_ids = set(old_dict)
    task_name = None
    for task_id in task_ids:
        old_status = old_dict[task_id]["status"]
        cur_status = cur_dict[task_id]["status"]
        if (old_status != "full" and cur_status == "full"):
            task_name = cur_dict[task_id]['title']
    

    return task_name


bot = telebot.TeleBot(os.getenv("TOKEN"))



for cses_id in cses_ids:
    db.update_user(cses_id)

def get_random_message(nickname, task):
    messages = [
    f"🎉 <code>{nickname}</code> успешно решил <i>{task}</i>!",
    f"<code>{nickname}</code> справился с задачей <i>{task}</i> ✅",
    f"Задача <i>{task}</i> покорилась <code>{nickname}</code> 💪",
    f"📘 <code>{nickname}</code> завершил <i>{task}</i>!",
    f"<i>{task}</i> — выполнено пользователем <code>{nickname}</code> 🚀",
    f"🥳 <code>{nickname}</code> закрыл задание <i>{task}</i>!",
    f"✅ <code>{nickname}</code> решил <i>{task}</i> как профи!",
    f"📚 <code>{nickname}</code> преодолел <i>{task}</i>!",
    f"🎯 Миссия <i>{task}</i> выполнена! Исполнитель — <code>{nickname}</code>.",
    f"<code>{nickname}</code> добавил в коллекцию решённых задач: <i>{task}</i> 🧠",
    ]
    return random.choice(messages)


while True:
    for cses_id in cses_ids:
        try:
            task = check_for_solved_task(cses_id)
            if(task != None):
                nickname = cses_client.get_user_nickname(cses_id)
                try:
                    bot.send_message(os.getenv("CHANNEL_ID"), text=get_random_message(nickname, task), parse_mode='HTML')
                    print(nickname, task)
                    db.update_user(cses_id)
                except Exception as e:
                    print(f"[ERROR] Failed to send Telegram message: {e}")
        except Exception as e:
            print(f"[ERROR] Problem with cses_id {cses_id}: {e}")
    print("Проверено ✅")
    time.sleep(10)