from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Course


class CourseTestCase(APITestCase):

    def setUp(self):

        self.user = User.objects.create(username="test_user")

        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(title="Test Course", owner=self.user)

    def test_create_course(self):

        data = {"title": "New Course", "description": "Test"}

        response = self.client.post("/courses/", data)

        self.assertEqual(response.status_code, 201)
