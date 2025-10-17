# CSES Telegram Bot

**CSES Telegram Bot** — это сервис, который отслеживает решения задач пользователями на сайте [CSES](https://cses.fi/) и отправляет уведомления в Telegram, когда кто-то решает задачу.  

Сервис работает с использованием **Docker Compose** для удобного разворачивания.

---

## Функционал

- Парсит сайт CSES и проверяет, какие задачи решили указанные пользователи.  
- Отслеживает новые решения и отправляет уведомления в Telegram-группу.  
- Полностью настраивается через `.env` файл.

---

## Требования

- Docker  
- Docker Compose  
- Telegram бот и группа (для отправки уведомлений)  

---

## Установка

1. Склонируйте репозиторий:

```bash
git clone https://github.com/yourusername/cses-tracker-bot.git
cd cses-tracker-bot
```


2. Создайте файл `.env` и заполните его:

```env
MONGO_INITDB_ROOT_USERNAME=пароль_для_базы_данных
MONGO_INITDB_ROOT_PASSWORD=логин_для_базы_данных
CSES_USERNAME=логин_cses_fi
CSES_PASSWORD=пароль_cses_fi
TOKEN=токен_бота_в_телеграмм
CHANNEL_ID=id_чата_или_канала
```


3. Запустите проект через Docker Compose:

```bash
docker-compose up -d
```

---

## Использование

После запуска бот автоматически проверяет решения пользователей и отправляет уведомления в указанную группу Telegram.

Пример уведомления:

```
📘 Ezegor завершил Two Knights!
```

---

