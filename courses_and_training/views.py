from rest_framework import viewsets, generics
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsModerator, IsOwner
from rest_framework.permissions import IsAuthenticated


# CRUD для курса через ViewSet
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):

        if self.action == "create":
            permission_classes = [IsAuthenticated, ~IsModerator]

        elif self.action == "destroy":
            permission_classes = [IsAuthenticated, IsOwner]

        elif self.action in ["update", "partial_update"]:
            permission_classes = [IsAuthenticated, IsModerator | IsOwner]

        elif self.action in ["retrieve", "list"]:
            permission_classes = [IsAuthenticated]

        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


# CRUD для уроков через Generic-классы
class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

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
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    def get_permissions(self):

        if self.request.method in ["PUT", "PATCH"]:
            permission_classes = [IsAuthenticated | IsModerator]

        elif self.request.method == "DELETE":
            permission_classes = [IsOwner]

        else:
            permission_classes = [IsAuthenticated | IsModerator]

        return [permission() for permission in permission_classes]
