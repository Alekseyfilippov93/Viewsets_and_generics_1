from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="habits"
    )
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_reward_habit = models.BooleanField(default=False)
    related_habit = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="linked_habits",
    )
    reward = models.CharField(max_length=255, blank=True, null=True)
    frequency_days = models.PositiveSmallIntegerField(default=1)
    duration_seconds = models.PositiveSmallIntegerField(default=60)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    telegram_chat_id = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        # Нельзя одновременно указать reward и related_habit
        if self.reward and self.related_habit:
            raise ValidationError(
                "Нельзя одновременно указывать reward и related_habit."
            )

        # Приятная привычка не должна иметь reward или related_habit
        if self.is_reward_habit and (self.reward or self.related_habit):
            raise ValidationError(
                "Приятная привычка не может иметь reward или related_habit."
            )

        # Связанная привычка должна быть приятной
        if self.related_habit and not self.related_habit.is_reward_habit:
            raise ValidationError("Связанная привычка должна быть приятной.")

        # Время на выполнение ≤ 120 секунд
        if self.duration_seconds > 120:
            raise ValidationError(
                "Время выполнения привычки не может быть больше 120 секунд."
            )

        # Периодичность ≥ 1 и ≤7 дней
        if self.frequency_days < 1 or self.frequency_days > 7:
            raise ValidationError(
                "Периодичность выполнения должна быть от 1 до 7 дней."
            )

    def save(self, *args, **kwargs):
        self.full_clean()  # запуск валидаторов перед сохранением
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} — {self.action} в {self.time}"
