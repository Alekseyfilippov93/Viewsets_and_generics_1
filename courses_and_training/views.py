from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsModerator, IsOwner, IsOwnerOrModerator
from .paginators import CoursePagination

from .tasks import send_course_update_email
from django.utils import timezone
from datetime import timedelta


# CRUD для курса через ViewSet
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):

        if self.action in ["update", "partial_update", "retrieve", "list"]:
            permission_classes = [IsAuthenticated | IsModerator]

        elif self.action in ["create", "destroy"]:
            permission_classes = [IsAuthenticated]

        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def perform_update(self, serializer):
        course = serializer.save()

        if course.updated_at and timezone.now() - course.updated_at < timedelta(
            hours=4
        ):
            return

        subscriptions = Subscription.objects.filter(course=course)
        emails = [sub.user.email for sub in subscriptions]

        if emails:
            send_course_update_email.delay(emails, course.title)


# CRUD для уроков через Generic-классы
class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]
    pagination_class = CoursePagination

    def get_permissions(self):

        if self.request.method == "POST":
            permission_classes = [IsAuthenticated]

        else:
            permission_classes = [IsAuthenticated | IsModerator]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]


class SubscriptionAPIView(APIView):

    def post(self, request):

        user = request.user
        course_id = request.data.get("course_id")

        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "подписка добавлена"

        return Response({"message": message})
