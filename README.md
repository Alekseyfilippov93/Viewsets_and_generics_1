# Habit Tracker

Простое API для отслеживания привычек на Django REST Framework.

---

## Функционал

- CRUD привычек (создание, просмотр, редактирование, удаление)
- Публичные привычки (доступны без авторизации)
- Валидация данных (ограничения на длительность, периодичность)
- JWT аутентификация
- Swagger документация
- Пагинация
- Celery

---

## Стек

- Python
- Django
- Django REST Framework
- PostgreSQL
- JWT (SimpleJWT)

---

## Запуск проекта

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка .env

```commandline
SECRET_KEY=your_secret_key
DEBUG=True

DB_NAME=your_db
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

TELEGRAM_BOT_TOKEN=your_token
```

### 3. Применить миграции

```commandline
python manage.py migrate
```

### 4. Создать суперпользователя

```commandline
python manage.py createsuperuser
```

### 4. Запустить сервер

```commandline
python manage.py runserver
```

## API

Swagger документация:
http://127.0.0.1:8000/api/docs/

---

### Аутентификация

#### Получить токен:

- POST /api/token/
  Пример:

```
{
  "email": "user@example.com",
  "password": "password"
}
```

#### Использовать токен:

```
Authorization: Bearer <token>
```

#### Эндпоинты

- GET /api/habits/ — список привычек пользователя
- POST /api/habits/ — создать привычку
- PATCH /api/habits/{id}/ — обновить
- DELETE /api/habits/{id}/ — удалить
- GET /api/habits/public/ — публичные привычки

## Тесты

```
python manage.py test habits
```