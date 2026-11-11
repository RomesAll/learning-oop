"""
D — Dependency Inversion Principle (Принцип инверсии зависимостей)
Определение:

Модули верхних уровней не должны зависеть от модулей нижних уровней. Оба типа модулей должны зависеть от абстракций.
Абстракции не должны зависеть от деталей. Детали должны зависеть от абстракций.

Простыми словами: Наш основной бизнес-код не должен жестко привязываться к конкретным библиотекам,
базам данных или внешним сервисам (платежным системам, почтовым клиентам).
Вместо этого мы связываем код через интерфейсы (абстракции).

Это позволяет легко подменять одни компоненты на другие без переписывания бизнес-логики.

Ну т.е. классы должны быть связаны агрегацией
"""
from abc import ABC, abstractmethod


# 1. Абстракция (интерфейс, который задает единый контракт)
class PaymentGateway(ABC):

    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass


# 2. Низкоуровневые детали реализуют этот интерфейс
class StripeGateway(PaymentGateway):

    def process_payment(self, amount: float) -> bool:
        print(f"Списание {amount} руб. через Stripe...")
        return True


class PayPalGateway(PaymentGateway):

    def process_payment(self, amount: float) -> bool:
        print(f"Списание {amount} руб. через PayPal...")
        return True


# 3. Высокоуровневый модуль зависит ТОЛЬКО от абстракции
class OrderService:

    def __init__(self, payment_gateway: PaymentGateway):
        # Мы принимаем интерфейс, а не конкретную реализацию!
        self.payment_gateway = payment_gateway

    def checkout(self, amount: float):
        print("Проверка товаров, расчет скидок...")
        self.payment_gateway.process_payment(amount)