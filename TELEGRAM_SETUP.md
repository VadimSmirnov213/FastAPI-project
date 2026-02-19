# Настройка Telegram уведомлений

## Шаг 1: Создание бота

1. Откройте Telegram и найдите **@BotFather**
2. Отправьте команду `/newbot`
3. Следуйте инструкциям:
   - Введите имя бота (например: "Dev Studio Notifications")
   - Введите username бота (должен заканчиваться на `bot`, например: `dev_studio_notifications_bot`)
4. Сохраните полученный **токен бота** (выглядит как: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

## Шаг 2: Получение Chat ID

Есть несколько способов получить ваш Chat ID:

### Способ 1: Через @userinfobot
1. Найдите бота **@userinfobot** в Telegram
2. Отправьте ему любое сообщение
3. Он вернет ваш Chat ID (число, например: `123456789`)

### Способ 2: Через вашего бота
1. Начните диалог с вашим ботом (найдите его по username)
2. Отправьте боту любое сообщение (например: `/start`)
3. Откройте в браузере: `https://api.telegram.org/bot<ВАШ_ТОКЕН>/getUpdates`
4. Найдите в ответе `"chat":{"id":123456789}` - это ваш Chat ID

### Способ 3: Через @getidsbot
1. Найдите бота **@getidsbot**
2. Отправьте ему любое сообщение
3. Он вернет ваш Chat ID

## Шаг 3: Настройка .env файла

Создайте файл `.env` в папке `backend/` и добавьте:

```env
# Telegram настройки
TELEGRAM_BOT_TOKEN=ваш_токен_бота_от_BotFather
TELEGRAM_CHAT_ID=ваш_chat_id
TELEGRAM_ENABLED=true
```

**Пример:**
```env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
TELEGRAM_ENABLED=true
```

## Шаг 4: Перезапуск сервера

После настройки перезапустите сервер:

```bash
python3 run.py
```

## Проверка работы

1. Отправьте тестовую заявку через форму на сайте
2. Проверьте, что сообщение пришло в Telegram

## Отключение уведомлений

Чтобы временно отключить уведомления, установите в `.env`:
```env
TELEGRAM_ENABLED=false
```

Или просто не указывайте `TELEGRAM_BOT_TOKEN` и `TELEGRAM_CHAT_ID`.

