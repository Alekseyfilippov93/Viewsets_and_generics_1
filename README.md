# Viewsets_and_generics

## Описание

Backend-приложение для управления курсами и уроками.

## О проекте

Проект реализован на Django REST Framework и включает:

- авторизацию JWT;
- роли пользователей и права доступа;
- CRUD для курсов и уроков;
- оплату;
- Celery-задачи;
- Celery Beat для периодических задач;
- Docker-контейнеризацию;
- CI/CD с автоматическим деплоем на сервер.

## Стек

- Python 3.13
- Django
- Django REST Framework
- Poetry
- Docker / Docker Compose
- PostgreSQL
- Redis
- Celery
- Celery Beat
- Nginx
- GitHub Actions

## Установка

```bash
git clone <repo_url>
cd Viewsets_and_generics
```

---

## Сериализаторы

- **Модель Payment (users)**
    - user — ссылка на пользователя
    - payment_date — дата оплаты
    - paid_course — оплаченный курс
    - paid_lesson — оплаченный урок
    - amount — сумма оплаты
    - payment_method — способ оплаты (`cash` / `transfer`)

- **Фикстура payments.json** для добавления тестовых данных

- **API эндпоинт `/api/payments/`** через DRF ViewSet и сериализатор

---

## Система авторизации и прав доступа

В проекте реализована JWT-авторизация и гибкая система прав доступа.

### Авторизация

Используется библиотека **SimpleJWT**.

Доступные эндпоинты:

- Регистрация пользователя
- Получение JWT токена (/api/register/)
- Обновление токена (/api/token/)
- Все остальные эндпоинты защищены авторизацией (/api/token/refresh/)

---

### Роли пользователей

В системе реализованы две роли:

#### Пользователь

- может создавать курсы и уроки
- может редактировать и удалять **только свои объекты**

#### Модератор

- может просматривать любые курсы и уроки
- может редактировать любые курсы и уроки
- **не может создавать или удалять объекты**

---

### Владельцы объектов

В моделях `Course` и `Lesson` реализовано поле владельца:
owner = ForeignKey(User)
При создании объекта владелец автоматически назначается текущим пользователем.

---

### Permissions

Используются кастомные permissions:

- `IsModerator`
- `IsOwner`

Комбинация прав реализована через операторы DRF:
IsModerator | IsOwner
~IsModerator

---

### Фикстуры

Создана фикстура для групп пользователей:

---

### Валидация ссылок

Добавлен кастомный валидатор, который запрещает добавление ссылок на сторонние ресурсы.  
Разрешены только ссылки на `youtube.com`.

#### Валидатор реализован в файле:

courses/validators.py и подключён в сериализаторе уроков.

---

## Celery и фоновые задачи

- Настроен Celery с Redis для асинхронного выполнения задач;
- Добавлена асинхронная рассылка уведомлений пользователям при обновлении курса (не чаще чем раз в 4 часа)
- Настроен Celery Beat для периодических задач:
    - деактивация пользователей, которые не заходили более месяца (is_active=False)
- Временные зоны Django и Celery синхронизированы для корректного запуска задач.

---

## Docker и запуск проекта

---

### Проект полностью контейнеризован. Все сервисы запускаются одной командой.

- Создать файл .env (cp .env.example .env)
- Запустить проект (docker-compose up --build)

### Сервисы, которые поднимаются:

- backend — Django приложение
- db — PostgreSQL
- redis — Redis для Celery
- celery — обработчик фоновых задач
- celery-beat — планировщик периодических задач

### Доступ к сервисам

- Backend: http://localhost:8000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

#### Проверка работы сервисов

- Django

```
docker exec -it django_app python manage.py check
```

- PostgreSQL

```
docker exec -it postgres_db psql -U postgres
```

- Redis

```
- docker exec -it redis redis-cli ping
```

- Ожидаемый ответ:
  ```PONG```
- Celery Worker

```
-docker logs celery_worker
```

- Celery Beat

```
docker logs celery_beat
```

- Остановка проекта

```
docker-compose down
```

#### Переменные окружения

- Все чувствительные данные вынесены в файл .env.
- Пример файла находится в .env.example.

### Примечание

1. Клонируем репозиторий и переходим в папку проекта

```
git clone <repo_url>
cd Viewsets_and_generics
```

2. Создаём файл .env на основе шаблона

```
cp .env.example .env
```

3. Запуск проекта со сборкой контейнеров

```
docker-compose up --build
```

### Проект поднимет:

- backend — Django;
- db — PostgreSQL;
- redis — Redis;
- celery — worker;
- celery-beat — scheduler;
- nginx — reverse proxy.