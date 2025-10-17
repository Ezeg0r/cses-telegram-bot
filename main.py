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


with open("cses_ids.txt", "r") as f:
    cses_ids = [int(line.strip()) for line in f if line.strip()]

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
        f"🎉 <code>{nickname}</code> successfully solved <i>{task}</i>!",
        f"<code>{nickname}</code> completed the task <i>{task}</i> ✅",
        f"The task <i>{task}</i> was conquered by <code>{nickname}</code> 💪",
        f"📘 <code>{nickname}</code> finished <i>{task}</i>!",
        f"<i>{task}</i> — completed by <code>{nickname}</code> 🚀",
        f"🥳 <code>{nickname}</code> closed the assignment <i>{task}</i>!",
        f"✅ <code>{nickname}</code> solved <i>{task}</i> like a pro!",
        f"📚 <code>{nickname}</code> overcame <i>{task}</i>!",
        f"🎯 Mission <i>{task}</i> accomplished! Performer — <code>{nickname}</code>.",
        f"<code>{nickname}</code> added <i>{task}</i> to their collection of solved problems 🧠",
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