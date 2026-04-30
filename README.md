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
cp .env.example .env
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

- Запустить проект (docker compose up --build)

### Сервисы, которые поднимаются:

- backend — Django приложение
- db — PostgreSQL
- redis — Redis для Celery
- celery — обработчик фоновых задач
- celery-beat — планировщик периодических задач
- nginx — reverse proxy

### Доступ к сервисам

- Backend: http://localhost:8000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

#### Проверка работы сервисов

- Django

```
docker compose exec backend python manage.py check
```

- Миграции

```
docker compose exec backend python manage.py migrate
```

- PostgreSQL

```
docker compose exec db psql -U postgres
```

- Redis

```
docker compose exec redis redis-cli ping
```

- Ожидаемый ответ:
  ```PONG```

- Celery Beat

```
docker compose logs -f celery-beat
```

- Остановка проекта

```
docker compose down
```

#### Переменные окружения

- Все чувствительные данные вынесены в файл ```.env```
- Пример файла находится в ```.env.example```

Основные переменные:

- SECRET_KEY
- DEBUG
- ALLOWED_HOSTS
- POSTGRES_DB
- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_HOST
- POSTGRES_PORT
- STRIPE_SECRET_KEY
- CELERY_BROKER_URL
- CELERY_RESULT_BACKEND

---

### CI/CD и деплой на сервер

В проекте настроен CI/CD с помощью GitHub Actions.

#### Pipeline включает:

- lint — проверка качества кода;
- test — запуск тестов проекта;
- build — проверка возможности сборки Docker-образов;
- deploy — автоматический деплой на сервер по SSH после успешного прохождения всех проверок.

Что нужно для деплоя
В secrets репозитория GitHub должны быть добавлены:

- SERVER_IP — IP-адрес сервера;
- SERVER_USER — пользователь для SSH;
- SSH_KEY — приватный SSH-ключ.

Что должно быть настроено на сервере

- установлен Docker;
- установлен Docker Compose;
- открыт SSH-доступ;
- подготовлена папка с проектом.

**Как выполняется деплой**
После успешного прохождения всех jobs GitHub Actions подключается к серверу по SSH и выполняет:

```
git pull
docker compose down
docker compose up -d --build
```


