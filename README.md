# Telegram Bot with Admin Panel

Этот бот для Telegram позволяет управлять командами через админ-панель. Он поддерживает HTML-разметку в ответах, а также имеет функцию автоматического уведомления о времени работы.

## 📌 Функции
- 🔹 Добавление и удаление команд через админ-панель
- 🔹 Отправка сообщений с HTML-разметкой
- 🔹 Вывод uptime бота
- 🔹 Автоматическая отправка uptime каждые 10 часов
- 🔹 Логирование ошибок и их отправка админу

## 🚀 Установка и запуск

### 1️⃣ Клонирование репозитория
```bash
git clone https://github.com/your-repo/telegram-bot.git
cd telegram-bot
```

### 2️⃣ Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3️⃣ Настройка бота
1. Получите токен у [@BotFather](https://t.me/BotFather) и замените `TOKEN` в коде.
2. Укажите ваш Telegram ID в `ADMIN_ID`.

### 4️⃣ Запуск бота
```bash
python bot.py
```

## 🔧 Использование

### Добавление команды
```bash
/add команда текст ответа
```
Пример:
```
/add привет Привет, как дела?
```

### Удаление команды
1. Отправьте `/admin`
2. Выберите "❌ Удалить команду"
3. Нажмите на нужную команду

### Проверка времени работы
```bash
/uptime
```

## 📂 Файлы
- `bot.py` — основной код бота
- `commands.json` — хранилище команд
- `requirements.txt` — список зависимостей

## 📜 Лицензия
Этот проект распространяется под MIT License.

