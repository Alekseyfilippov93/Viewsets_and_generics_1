from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet,
    LessonListCreateAPIView,
    LessonRetrieveUpdateDestroyAPIView,
    SubscriptionAPIView,
)

router = DefaultRouter()
router.register(r"courses", CourseViewSet)

urlpatterns = [
    path("lessons/", LessonListCreateAPIView.as_view()),
    path("lessons/<int:pk>/", LessonRetrieveUpdateDestroyAPIView.as_view()),
    path("subscribe/", SubscriptionAPIView.as_view()),
]

urlpatterns += router.urls
