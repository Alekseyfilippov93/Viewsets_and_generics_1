from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """Класс проверяет находиться ли пользователь в модераторах"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderators").exists()


class IsOwner(BasePermission):
    """Класс проверяет является ли пользователь владельцем объекта"""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
