# Backend - FastAPI

Бэкенд API для веб-приложения на FastAPI.

## Установка

1. Python 3.10+

2. Установка python3-venv:
```bash
sudo apt install python3-venv
```

3. Создание виртуального окружения:
```bash
python3 -m venv venv
```

4. Активация виртуального окружение:
```bash
source venv/bin/activate
```

5. Установка зависимостей:
```bash
pip install -r requirements.txt
```

6. Создание `.env`:
```bash
cp .env.example .env
```

## Запуск

### Режим разработки

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Или:
```bash
python3 run.py
```

API будет доступен по адресу: [http://localhost:8000](http://localhost:8000)

### Production

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Документация

После запуска сервера доступна документация:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Структура проекта

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Точка входа приложения
│   ├── config.py            # Конфигурация
│   ├── database.py          # Настройка БД
│   ├── models.py            # SQLAlchemy модели
│   ├── schemas.py           # Pydantic схемы
│   └── api/
│       ├── __init__.py
│       ├── projects.py      # API для проектов
│       ├── contacts.py      # API для контактов
│       ├── health.py        # Health check
│       └── dependencies.py  # Зависимости
├── requirements.txt
├── .env.example
└── README.md
```

## API

### Health Check
- `GET /api/v1/health` - Health cheak

### Projects (Проекты)
- `GET /api/v1/projects` - Получить список проектов
  - Query параметры: `skip`, `limit`, `category`, `featured`
- `GET /api/v1/projects/{id}` - Получить проект по ID
- `POST /api/v1/projects` - Создать новый проект
- `PUT /api/v1/projects/{id}` - Обновить проект
- `DELETE /api/v1/projects/{id}` - Удалить проект

### Contacts (Контакты)
- `POST /api/v1/contacts` - Создать обращение из формы
- `GET /api/v1/contacts` - Получить список обращений (для админки)
  - Query параметры: `skip`, `limit`, `unread_only`
- `GET /api/v1/contacts/{id}` - Получить обращение по ID
- `PATCH /api/v1/contacts/{id}/read` - Отметить как прочитанное
- `DELETE /api/v1/contacts/{id}` - Удалить обращение

## DB

По умолчанию используется SQLite. DB создается автоматически при первом запуске в файле `dev_studio.db`.

Для использования PostgreSQL изменить `DATABASE_URL` в `.env`:
```
DATABASE_URL=postgresql://user:password@localhost/dbname
```

## Настройка

Все настройки изменяются в файле `.env`:

- `DATABASE_URL` - URL базы данных
- `CORS_ORIGINS` - Разрешенные источники для CORS
- `HOST` - Хост сервера
- `PORT` - Порт сервера


### Проверка работы Telegram

После настройки проверка работы через тестовый эндпоинт:

```bash
curl http://localhost:8000/api/v1/telegram/test
```

Или: [http://localhost:8000/api/v1/telegram/test](http://localhost:8000/api/v1/telegram/test)

Этот эндпоинт показывает:
- Текущую конфигурацию Telegram
- Отправку тестового сообщения
- Errors

Проверка конфигурации:
```bash
curl http://localhost:8000/api/v1/telegram/config
```


## Примеры запросов

### Создать проект
```bash
curl -X POST "http://localhost:8000/api/v1/projects" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "E-commerce платформа",
    "description": "Платформа",
    "category": "Веб-разработка",
    "year": "2024",
    "tags": ["Next.js", "TypeScript", "Stripe"]
  }'
```

### Отправить контактную форму
```bash
curl -X POST "http://localhost:8000/api/v1/contacts" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Name Name",
    "email": "ivan@example.com",
    "phone": "+7 (999) 123-45-67",
    "message": "mess"
  }'
```

## P.S. - архитектура далеко не правильная, проект под личные цели за сжатые сроки
