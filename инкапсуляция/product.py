import pytest


class Product:
    """Класс для хранения инф. о продуктах"""

    def __init__(self, name: str, price: float):
        self.name = name
        self._price = 0.0 # защищенный атрибут
        self.price = price # механизм инкапсуляции

    """
    Смотри, если бы вместо _price был изменяемый объект, то
    возвращать оригинальный объект - это нарушение инкапсуляции, поэтому
    нужно возвращать копию объекта через copy() или deepcopy()
    
    Вот пример работы с такими объектами:
    
    class Order:
    
        def __init__(self, customer_email: str):
            self.customer_email = customer_email
            self._items = []  # Приватный список товаров, закрыт от прямого доступа
    
        # Геттер возвращает только КОПИЮ или ТУПЛ, защищая от внешних изменений
        @property
        def items(self) -> tuple:
            return tuple(self._items)
    
        # 1. Контролируемое добавление элемента
        def add_item(self, name: str, price: float, quantity: int = 1):
            if price <= 0:
                raise ValueError("Цена товара должна быть больше нуля!")
            if quantity <= 0:
                raise ValueError("Количество должно быть положительным!")
    
            # Проверяем бизнес-логику (например, нет ли уже такого товара)
            for item in self._items:
                if item["name"] == name:
                    # Если товар уже есть, просто увеличиваем количество
                    item["quantity"] += quantity
                    return
    
            # Если товара нет — добавляем новый
            self._items.append(
                {"name": name, "price": price, "quantity": quantity}
            )
    
        # 2. Контролируемое удаление элемента
        def remove_item(self, name: str):
            self._items = [item for item in self._items if item["name"] != name]
    
        # Метод для расчета итоговой суммы
        def get_total(self) -> float:
            return sum(item["price"] * item["quantity"] for item in self._items)
    """

    @property
    def price(self):
        return self._price


    @price.setter
    def price(self, value: float):
        # нельзя передать отрицательное значение
        if value < 0.0:
            raise ValueError("Цена не может быть отрицательной!")
        self._price = value


if __name__ == '__main__':
    product = Product(name='milk', price=123.1)

    assert product.price == 123.1


    with pytest.raises(ValueError):
        product.price = -10.0