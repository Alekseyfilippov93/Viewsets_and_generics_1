from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Payment
from .serializers import PaymentSerializer
from rest_framework import generics, viewsets
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer
from .services import create_product, create_price, create_checkout_session

User = get_user_model()


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["paid_course", "paid_lesson", "payment_method"]
    ordering_fields = ["payment_date"]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        if payment.paid_course:
            name = payment.paid_course.title
        else:
            name = payment.paid_lesson.title

        product = create_product(name)
        price = create_price(product.id, payment.amount)
        session = create_checkout_session(price.id)

        payment.payment_url = session.url
        payment.save()
