"""
Задача написать классы, которые будут удовлетворять принципу
Single responsibility principle
"""

class Order:
    """Класс для хранения данных заказа и расчет."""

    def __init__(self, items: list, user_email: str):
        self._items = items
        self._user_email = user_email

    def calc_total(self) -> float:
        """Посчитать итоговую стоимость товара."""
        return sum(item['price'] * item['quantity'] for item in self._items)


class OrderRepository:
    """Репозиторий для доступа к данным товаров."""

    def __init__(self, session: object):
        self._session = session

    def save(self, order: Order):
        """Сохранить информацию о товаре."""
        print(f'Товар {order} успешно сохранен')


class PaymentProcessor:
    """Класс для осуществления платежей."""

    def processing(self, order: Order, card_num: int):
        """Провести платеж за товар."""
        print(f'Товар {order} успешно оплачен')

