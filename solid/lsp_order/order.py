"""
Определение: Если класс B является подтипом класса A, то объекты типа A в программе можно заменить на объекты типа
B без изменения желаемых свойств программы.
Простыми словами: Наследник должен дополнять родителя, но не ломать его поведение. Если код работает с базовым классом,
он должен корректно работать с любым из его дочерних классов, не ожидая сюрпризов (вроде внезапных ошибок или исключений).
"""

from abc import ABC, abstractmethod


class Product(ABC):
    """Базовый класс продуктов"""

    def __init__(self, name: str, price: int):
        self._name = name
        self._price = price

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

"""
Дочерние классы могу быть заменены родительским без
исключительных ситуаций
"""

class PhysicalProduct(Product):
    """Дочерний класс продуктов"""
    def __init__(self, name: str, price: int, weight: int):
        super().__init__(name, price)
        self._weight = weight

    def get_shipping_cost(self):
        return self._weight * 100


class DigitalProduct(Product):
    """Дочерний класс продуктов"""
    pass