from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """Класс проверяет находиться ли пользователь в модераторах"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderators").exists()
