# Viewsets_and_generics

## Описание

Backend-приложение для управления курсами и уроками.

## Стек

- Python
- Django
- Django REST Framework
- Poetry

## Установка

```bash
git clone <repo_url>
cd project
poetry install
```

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

