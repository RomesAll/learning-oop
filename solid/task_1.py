"""
🛠 Комплексная задача: Рефакторинг «Божественного объекта» (God Object)

import sqlite3

class OrderManager:
    def __init__(self, items: list, customer_email: str, customer_type: str):
        self.items = items
        self.customer_email = customer_email
        self.customer_type = customer_type

    # 1. Считает сумму и скидку (Смешана бизнес-логика и разные типы скидок)
    def calculate_total(self) -> float:
        total = sum(item["price"] * item["quantity"] for item in self.items)

        if self.customer_type == "regular":
            return total * 0.95
        elif self.customer_type == "vip":
            return total * 0.80
        elif self.customer_type == "employee":
            return total * 0.50
        return total

    # 2. Сохранение в базу данных (Жесткая привязка к конкретной SQLite)
    def save_to_db(self):
        conn = sqlite3.connect("shop.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO orders (email, total) VALUES (?, ?)", (self.customer_email, self.calculate_total()))
        conn.commit()
        conn.close()

    # 3. Проведение оплаты (Жесткая привязка к конкретному Stripe API)
    def process_payment(self, card_number: str):
        total = self.calculate_total()
        print(f"Списание {total} руб. через Stripe с карты {card_number}")
        # Вызов реального Stripe API...

    # 4. Отправка уведомлений
    def send_notification(self):
        print(f"Отправка email на {self.customer_email}: Ваш заказ принят!")

    # 5. Управление доставкой
    def calculate_shipping(self, weight: float, is_digital: bool) -> float:
        if is_digital:
            raise Exception("Цифровые товары не доставляются курьером!")
        return weight * 150
"""

from abc import ABC, abstractmethod


# 1. Интерфейс для расчета скидок (OCP)
class DiscountStrategy(ABC):

    @abstractmethod
    def calculate(self, total: float) -> float:
        pass


class RegularDiscount(DiscountStrategy):

    def calculate(self, total: float) -> float:
        return total * 0.95


class VIPDiscount(DiscountStrategy):

    def calculate(self, total: float) -> float:
        return total * 0.80


class EmployeeDiscount(DiscountStrategy):

    def calculate(self, total: float) -> float:
        return total * 0.50


class NoDiscount(DiscountStrategy):

    def calculate(self, total: float) -> float:
        return total


class Order:
    def __init__(self, items, customer_email):
        self.items = items
        self.customer_email = customer_email

    def get_subtotal(self) -> float:
        return sum(item["price"] * item["quantity"] for item in self.items)

    def calculate_total(self, discount_strategy: DiscountStrategy) -> float:
        subtotal = self.get_subtotal()
        return discount_strategy.calculate(subtotal)


# Абстракция для сохранения
class OrderRepository(ABC):

    @abstractmethod
    def save(self, order: Order, total: float):
        pass


# Конкретная реализация для SQLite
class SQLiteOrderRepository(OrderRepository):

    def save(self, order: Order, total: float):
        print(
            f"Сохранение в SQLite: заказ для {order.customer_email}, сумма: {total}"
        )


# Абстракция для платежей
class PaymentGateway(ABC):

    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass


# Конкретный платежный шлюз (Stripe)
class StripePaymentGateway(PaymentGateway):

    def process_payment(self, amount: float) -> bool:
        print(f"Списание {amount} через Stripe API...")
        return True


discount_factory = {
    "regular": RegularDiscount(),
    "vip": VIPDiscount(),
    "employee": EmployeeDiscount(),
    "none": NoDiscount(),
}


if __name__ == '__main__':
    # 1. Создаем заказ
    my_order = Order(
        items=[{"price": 2000, "quantity": 1}], customer_email="client@shop.ru"
    )

    # 2. Выбираем стратегию скидки (например, VIP)
    discount = VIPDiscount()
    total_amount = my_order.calculate_total(discount)

    # 3. Инъецируем зависимости (DIP) в сервис обработки
    payment_gw = StripePaymentGateway()
    repository = SQLiteOrderRepository()

    # Проводим оплату и сохраняем через абстракции
    if payment_gw.process_payment(total_amount):
        repository.save(my_order, total_amount)
        print("Уведомление отправлено клиенту!")