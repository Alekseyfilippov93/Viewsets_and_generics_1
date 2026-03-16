import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY
# Сервисные функции взаимодействуют с платежным сервисом (Stripe)


def create_product(name):
    product = stripe.Product.create(name=name)
    return product


def create_price(product_id, amount):
    price = stripe.Price.create(
        product=product_id,
        unit_amount=int(amount * 100),
        currency="usd",
    )
    return price


def create_checkout_session(price_id):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
    )

    return session
