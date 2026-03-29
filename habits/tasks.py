import requests
from celery import shared_task
from django.utils import timezone
from django.conf import settings
from .models import Habit

TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN


@shared_task
def send_habit_reminder(habit_id):
    try:
        habit = Habit.objects.get(id=habit_id)
    except Habit.DoesNotExist:
        return
    if habit.telegram_chat_id and TELEGRAM_BOT_TOKEN:
        message = f"Напоминание!\nДействие: {habit.action}\nМесто: {habit.place}\nВремя: {habit.time}"
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        try:
            response = requests.post(
                url,
                data={"chat_id": habit.telegram_chat_id, "text": message},
                timeout=10,
            )
            print(response.json())
        except requests.exceptions.RequestException as e:
            print("Ошибка при отправке сообщения:", e)


@shared_task
def check_habits():
    now = timezone.localtime().time()
    habits = Habit.objects.filter(time__hour=now.hour, time__minute=now.minute)
    for habit in habits:
        send_habit_reminder.delay(habit.id)
