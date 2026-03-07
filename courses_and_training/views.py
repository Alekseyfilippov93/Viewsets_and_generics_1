from rest_framework import viewsets, generics
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsModerator
from rest_framework.permissions import IsAuthenticated


# CRUD для курса через ViewSet
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):

        if self.action in ["update", "partial_update", "retrieve", "list"]:
            permission_classes = [IsAuthenticated | IsModerator]

        elif self.action in ["create", "destroy"]:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


# CRUD для уроков через Generic-классы
class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated | IsModerator]
