from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to="users/avatars/", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Payment(models.Model):
    CASH = "cash"
    TRANSFER = "transfer"

    PAYMENT_METHODS = [
        (CASH, "Наличные"),
        (TRANSFER, "Перевод на счет"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Пользователь",
    )

    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")

    paid_course = models.ForeignKey(
        "courses_and_training.Course",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="course_payments",
        verbose_name="Оплаченный курс",
    )

    paid_lesson = models.ForeignKey(
        "courses_and_training.Lesson",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lesson_payments",
        verbose_name="Оплаченный урок",
    )

    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Сумма оплаты"
    )

    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHODS, verbose_name="Способ оплаты"
    )

    payment_url = models.URLField(
        blank=True, null=True, verbose_name="Ссылка на оплату"
    )

    def __str__(self):
        return f"{self.user} - {self.amount}"
