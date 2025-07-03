import requests
from bs4 import BeautifulSoup
import re

class CsesClient:
    def __init__(self, nickname, password):
        try:
            self.session = requests.Session()
            
            #recivieng the csrf_token
            login_page = self.session.get("https://cses.fi/login").text
            soup = BeautifulSoup(login_page, 'html.parser')
            csrf_token = soup.find("input", {"name": "csrf_token"}).get("value")

            #login
            payload = {"nick": nickname, "pass": password, "csrf_token": csrf_token}
            response = self.session.post("https://cses.fi/login", data=payload)
            if response.status_code != 200:
                raise Exception("Login Failed")
        except Exception as e:
            print(f"[ERROR] Failed to initialize CsesClient: {e}")
            raise

    def get_user_tasks(self, cses_id):
        try:
            user_page = self.session.get(f"https://cses.fi/problemset/user/{cses_id}/").text
            soup = BeautifulSoup(user_page, 'html.parser')
            tasks = []
            for task in soup.find_all('a', {"class": ["task-score icon", "task-score icon full", "task-score icon zero"]}):
                class_tag = task.get('class')
                status = "none"
                if ("full" in class_tag): status = "full"
                if ("zero" in class_tag): status = "zero"
                tasks.append({
                    "id": int(task.get('href').split('/')[3]),
                    "title": task.get("title"),
                    "status": status,
                })
        except Exception as e:
            print(f"[ERROR] Failed to fetch tasks for user {cses_id}: {e}")
            return []
        return tasks

    def get_user_nickname(self, cses_id):
        user_page = self.session.get(f"https://cses.fi/user/{cses_id}/").text
        soup = BeautifulSoup(user_page, 'html.parser')
        nickname = soup.find('h1', string=re.compile("User")).text.split(" ")[1]
        return nickname