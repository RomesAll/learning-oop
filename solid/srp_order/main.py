from order import Order, OrderRepository, PaymentProcessor


if __name__ == '__main__':
    order_data = {
        'user': 'Roman',
        'product': 'Milk',
        'price': 100,
        'quantity': 5
    }
    order = Order(items=[order_data, order_data], user_email='test@gmail.com')
    print('order total: ', order.calc_total())
    OrderRepository(session=None).save(order)
    PaymentProcessor().processing(order, card_num=122232412342134)