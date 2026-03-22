from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import User


@shared_task
def deactivate_inactive_users():
    month_ago = timezone.now() - timedelta(days=30)

    users = User.objects.filter(last_login__lt=month_ago, is_active=True)

    users.update(is_active=False)
