from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_course_update_email(emails, course_title):
    send_mail(
        subject="Обновление курса",
        message=f"Курс '{course_title}' был обновлен!",
        from_email="test@example.com",
        recipient_list=emails,
    )
