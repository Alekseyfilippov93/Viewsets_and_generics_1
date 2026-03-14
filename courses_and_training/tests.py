from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from .models import Course, Lesson, Subscription


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="test@test.com", password="12345")
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title="Test Course", description="Test", owner=self.user
        )

    def test_create_course(self):
        data = {"title": "New Course", "description": "Test Course"}
        response = self.client.post("/api/courses/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_course_list(self):
        response = self.client.get("/api/courses/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_subscription(self):
        data = {"course_id": self.course.id}
        response = self.client.post("/api/subscribe/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )


class LessonCRUDTestCase(APITestCase):
    """
    Тесты CRUD для модели Lesson с учётом прав доступа.
    """

    def setUp(self):
        # Пользователи
        self.owner = User.objects.create_user(email="owner@test.com", password="12345")
        self.other_user = User.objects.create_user(
            email="other@test.com", password="12345"
        )

        # Курс и урок
        self.course = Course.objects.create(
            title="Test Course", description="Description", owner=self.owner
        )
        self.lesson = Lesson.objects.create(
            title="Lesson 1",
            description="Lesson Content",
            video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            course=self.course,
            owner=self.owner,
        )

    def test_create_lesson_owner(self):
        self.client.force_authenticate(user=self.owner)
        data = {
            "title": "New Lesson",
            "description": "New Content",
            "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "course": self.course.id,
        }
        response = self.client.post("/api/lessons/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_lesson_other_user(self):
        self.client.force_authenticate(user=self.other_user)
        data = {
            "title": "Other Lesson",
            "description": "Other Content",
            "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "course": self.course.id,
        }
        response = self.client.post("/api/lessons/", data)
        # Обычный пользователь может создавать уроки
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_lesson_owner(self):
        self.client.force_authenticate(user=self.owner)
        data = {"title": "Updated Lesson"}
        response = self.client.patch(f"/api/lessons/{self.lesson.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Updated Lesson")

    def test_update_lesson_other_user(self):
        self.client.force_authenticate(user=self.other_user)
        data = {"title": "Hacker Update"}
        response = self.client.patch(f"/api/lessons/{self.lesson.id}/", data)
        # Не админ и не модератор не может обновлять
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_lesson_owner(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(f"/api/lessons/{self.lesson.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_delete_lesson_other_user(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(f"/api/lessons/{self.lesson.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubscriptionTestCase(APITestCase):
    """
    Тесты подписки на курс.
    """

    def setUp(self):
        self.user = User.objects.create_user(email="test@test.com", password="12345")
        self.other_user = User.objects.create_user(
            email="other@test.com", password="12345"
        )
        self.course = Course.objects.create(
            title="Test Course", description="Description", owner=self.user
        )

    def test_subscribe_toggle(self):
        self.client.force_authenticate(user=self.user)
        # Создание подписки
        response = self.client.post("/api/subscribe/", {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )
        self.assertEqual(response.data["message"], "подписка добавлена")

        # Удаление подписки
        response = self.client.post("/api/subscribe/", {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )
        self.assertEqual(response.data["message"], "подписка удалена")

    def test_subscribe_other_user(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post("/api/subscribe/", {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            Subscription.objects.filter(
                user=self.other_user, course=self.course
            ).exists()
        )
