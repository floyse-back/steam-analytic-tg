# 🎮 Steam Analytic Telegram Bot

**Steam Analytic Telegram Bot** — це телеграм-інтерфейс до системи **[Steam Analytic Repository](https://github.com/floyse-back/SteamAnalytic)**, який дозволяє взаємодіяти з аналітикою Steam прямо з вашого Telegram. Бот спрощує доступ до важливої інформації про ігри, користувачів, знижки та інше — у зручному, візуальному форматі.

## 🚀 Посилання на справжнього бота

[👉 Перейти до Steam Telegram Bot](https://t.me/SteamAnalyticsBot)

### 📱 QR-код для швидкого доступу:
![QR-код до бота](https://github.com/user-attachments/assets/14ecbdeb-43ec-4167-afad-4226997712b3)

---

## 📢 Telegram-канал який веде:
[![Steam Telegram Channel](https://res.cloudinary.com/dgjz5nvuo/image/upload/v1754385784/24c57d3c-09c0-4081-b54a-8f0a52c56c83.png)](https://t.me/steam_news_ua)

---

## 🖼️ Скріншоти

> Тут ви можете побачити, як виглядає бот у дії.

### 📌 Меню:
![Скріншот головного меню](https://res.cloudinary.com/dgjz5nvuo/image/upload/v1754384865/7573f5ed-d109-4de2-afe7-cddb532da3fb.png)

## 🚀 Основні можливості

- 🕹️ **Steam**  
  Перегляд актуальної інформації про ігри, знижки, безкоштовні пропозиції, категорії тощо.

- 👤 **Player**  
  Отримання даних про профілі Steam-користувачів, включно з їхньою статистикою.

- 📄 **Profile**  
  Можливість зареєструватися, змінити свій Steam ID, керувати профілем, додавати улюблені ігри.

- 🔔 **Підписки**  
  Підписуйтесь на сповіщення про знижки, нові ігри або цікаві події у Steam.  
  Нотифікації надсилаються автоматично, щойно з'являється нова інформація.

---

## 🛠️ Технічні деталі
- **Бекенд**: [Steam Analytic REST API](https://github.com/username/steam-analytic)
- ![Aiogram](https://img.shields.io/badge/aiogram-3.21.0-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Docker](https://img.shields.io/badge/Docker-ready-blue)
![RabbitMQ](https://img.shields.io/badge/rabbitmq-4.1-yellow)
![Celery](https://img.shields.io/badge/Celery-background_tasks-yellowgreen)
![Alembic](https://img.shields.io/badge/Alembic-migrations-important)
---

## 📦 Розгортання
1. Клонуйте репозиторій:

```bash

git clone https://github.com/username/steam-analytic-tg.git
```
2. Створіть .env за зразком .env.prev
```
#.env Повинен містити
# Database URLs
# Формат для PostgreSQL: postgresql+asyncpg://user:password@host/dbname
ASYNC_DATABASE_URL="postgresql+asyncpg://user:password@localhost/dbname"
SYNC_DATABASE_URL="postgresql://user:password@localhost/dbname"

# Base URL для FastAPI застосунку (зовнішній або локальний)
BASE_URL="http://127.0.0.1:8000/"

# Telegram Bot API Token
TELEGRAM_API_TOKEN="your-telegram-bot-token"

# Steam облікові дані
STEAM_ANALYTIC_NAME="your-steam-username"
STEAM_ANALYTIC_PASSWORD="your-steam-password"
STEAM_EMAIL="your-steam-email@example.com"
STEAM_APPID="your-target-steam-appid"  # You User Steam Appid

# RabbitMQ для Celery (черга завдань)
RABBITMQ_CONNECTION="amqp://guest:guest@127.0.0.1"

# Celery конфігурація
CELERY_BROKER_URL="amqp://guest:guest@localhost:5672"
# В прикладі використовується RabbitMQ але це можна змінити на будь-який брокер повідомлень
CELERY_RESULT_BACKEND="rpc://"

# Telegram сповіщення (опційно)
CHAT_ID="your-telegram-chat-id"
CHANNEL_URL="https://t.me/your_channel_name"
```
3. Запустіть Docker та виконайте команду
```bash

docker-compose up -d --build
```
---
## 🔗 Пов'язані проєкти

### [Steam Analytic Repository](https://github.com/floyse-back/SteamAnalytic)

> ⚠️ **Дуже рекомендується використовувати разом з бекендом Steam Analytic**, оскільки Telegram-бот є лише клієнтською частиною системи. Без запущеного бекенду функціональність бота буде обмежена або повністю недоступна.
---
## 👨‍💻 Автор
### [floyse-back](https://github.com/floyse-back) — розробка, проєктування та документація.
