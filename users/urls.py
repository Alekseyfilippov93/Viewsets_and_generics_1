from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RegisterAPIView, PaymentViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"payments", PaymentViewSet)

urlpatterns = [
    path("register/", RegisterAPIView.as_view()),
]

urlpatterns += router.urls
