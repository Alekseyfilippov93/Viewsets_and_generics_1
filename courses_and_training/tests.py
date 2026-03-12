from rest_framework.test import APITestCase
from users.models import User
from .models import Course, Subscription
from rest_framework import status


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test@test.com",
            password="12345"
        )

        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title="Test Course",
            description="Test",
            owner=self.user
        )

    def test_create_course(self):
        data = {
            "title": "New Course",
            "description": "Test Course"
        }

        response = self.client.post("/api/courses/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_course_list(self):
        response = self.client.get("/api/courses/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_subscription(self):
        data = {
            "course_id": self.course.id
        }

        response = self.client.post("/api/subscribe/", data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(
            Subscription.objects.filter(
                user=self.user,
                course=self.course
            ).exists()
        )
