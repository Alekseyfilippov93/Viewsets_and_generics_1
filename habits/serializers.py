from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = [
            "id",
            "user",
            "place",
            "time",
            "action",
            "is_reward_habit",
            "related_habit",
            "reward",
            "frequency_days",
            "duration_seconds",
            "is_public",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]

    def validate(self, data):
        # Проверка reward и related_habit
        if data.get("reward") and data.get("related_habit"):
            raise serializers.ValidationError(
                "Нельзя одновременно указывать reward и related_habit."
            )

        # Приятная привычка не должна иметь reward или related_habit
        if data.get("is_reward_habit") and (
            data.get("reward") or data.get("related_habit")
        ):
            raise serializers.ValidationError(
                "Приятная привычка не может иметь reward или related_habit."
            )

        # Связанная привычка должна быть приятной
        related = data.get("related_habit")
        if related and not related.is_reward_habit:
            raise serializers.ValidationError(
                "Связанная привычка должна быть приятной."
            )

        # Время на выполнение ≤ 120 секунд
        if data.get("duration_seconds") and data["duration_seconds"] > 120:
            raise serializers.ValidationError(
                "Время выполнения привычки не может быть больше 120 секунд."
            )

        # Периодичность 1–7 дней
        freq = data.get("frequency_days")
        if freq and (freq < 1 or freq > 7):
            raise serializers.ValidationError(
                "Периодичность должна быть от 1 до 7 дней."
            )

        return data
