from rest_framework import viewsets, permissions, generics
from .models import Habit
from .serializers import HabitSerializer
from .paginators import HabitPagination


# Права доступа: только владелец может редактировать/удалять свои привычки
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


# CRUD для привычек
class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    pagination_class = HabitPagination

    def get_queryset(self):
        # Своих привычек текущего пользователя
        if self.action in ["list", "create"]:
            return Habit.objects.filter(user=self.request.user)
        # Редактирование/удаление
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [permissions.IsAuthenticated, IsOwner]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [perm() for perm in permission_classes]


# Список публичных привычек (только чтение)
class PublicHabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)
