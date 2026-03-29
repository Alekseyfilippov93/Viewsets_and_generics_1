from django.contrib import admin
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "action", "time", "is_public")
    list_filter = ("is_public", "is_reward_habit")
    search_fields = ("action", "place")
