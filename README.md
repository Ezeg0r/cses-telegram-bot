# CSES Telegram Bot

**CSES Telegram Bot** is a service that tracks users' problem solutions on [CSES](https://cses.fi/) and sends notifications to Telegram when someone solves a problem.

The service uses **Docker Compose** for easy deployment.

---

## Features

* Parses the CSES website and checks which problems specified users have solved.
* Monitors new solutions and sends notifications to a Telegram group.
* Fully configurable via a `.env` file.

---

## Requirements

* Docker
* Docker Compose
* Telegram bot and group (for sending notifications)

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/cses-telegram-bot.git
cd cses-telegram-bot
```

2. Create a `.env` file and fill it in:

```env
MONGO_INITDB_ROOT_USERNAME=database_username
MONGO_INITDB_ROOT_PASSWORD=database_password
CSES_USERNAME=cses_username
CSES_PASSWORD=cses_password
TOKEN=telegram_bot_token
CHANNEL_ID=chat_or_channel_id
```

3. Add user IDs to the `cses_ids.txt` file:

```cses_ids
192852
252177
252209
345370
283319
345367
252191
```

4. Start the project using Docker Compose:

```bash
docker-compose up -d
```

---

## Usage

After starting, the bot automatically checks users' solved problems and sends notifications to the specified Telegram group.

Example notification:

```
📘 Ezegor completed Two Knights!
```
