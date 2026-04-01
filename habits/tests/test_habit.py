from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from habits.models import Habit

User = get_user_model()


# ТЕСТЫ МОДЕЛИ


class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="password123"
        )

    def test_create_habit(self):
        habit = Habit.objects.create(
            user=self.user,
            action="Пить воду",
            place="Кухня",
            time=timezone.localtime().time(),
            duration_seconds=60,
        )

        self.assertEqual(habit.user.email, "test@example.com")
        self.assertEqual(habit.action, "Пить воду")
        self.assertFalse(habit.is_reward_habit)

    def test_validation_reward_and_related(self):
        reward_habit = Habit.objects.create(
            user=self.user,
            action="Чтение книги",
            place="Комната",
            time=timezone.localtime().time(),
            is_reward_habit=True,
        )

        with self.assertRaises(Exception):
            Habit.objects.create(
                user=self.user,
                action="Йога",
                place="Зал",
                time=timezone.localtime().time(),
                reward="Сладость",
                related_habit=reward_habit,
            )

    def test_duration_seconds_validation(self):
        with self.assertRaises(Exception):
            Habit.objects.create(
                user=self.user,
                action="Долгая медитация",
                place="Комната",
                time=timezone.localtime().time(),
                duration_seconds=200,
            )


# ТЕСТЫ API


class HabitAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="password123"
        )

        # ВАЖНО: авторизация
        self.client.force_authenticate(user=self.user)

        self.habit = Habit.objects.create(
            user=self.user,
            action="Прогулка",
            place="Парк",
            time=timezone.localtime().time(),
            duration_seconds=60,
        )

    def test_create_habit(self):
        url = reverse("habit-list")

        data = {
            "action": "Йога",
            "place": "Зал",
            "time": str(timezone.localtime().time()),
            "duration_seconds": 60,
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_habits(self):
        url = reverse("habit-list")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_update_habit(self):
        url = reverse("habit-detail", args=[self.habit.id])

        response = self.client.patch(url, {"action": "Бег"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, "Бег")

    def test_delete_habit(self):
        url = reverse("habit-detail", args=[self.habit.id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(id=self.habit.id).exists())


# ПУБЛИЧНЫЕ ПРИВЫЧКИ


class PublicHabitAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="password123"
        )

        Habit.objects.create(
            user=self.user,
            action="Чтение",
            place="Комната",
            time=timezone.localtime().time(),
            duration_seconds=60,
            is_public=True,
        )

        Habit.objects.create(
            user=self.user,
            action="Прогулка",
            place="Парк",
            time=timezone.localtime().time(),
            duration_seconds=60,
            is_public=False,
        )
