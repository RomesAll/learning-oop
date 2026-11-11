from order import *


if __name__ == '__main__':
    # Оплачиваем через Stripe
    stripe_order = OrderService(StripeGateway())
    stripe_order.checkout(2500.0)

    # Оплачиваем через PayPal — код OrderService изменять не пришлось вообще!
    paypal_order = OrderService(PayPalGateway())
    paypal_order.checkout(2500.0)