"""
Дескрипторы в Python (Descriptors)

Определение: Дескриптор — это класс, который реализует хотя бы один из
магических методов протокола дескрипторов: __get__, __set__, или __delete__.

Простыми словами: Дескриптор позволяет вынести логику чтения и записи атрибута в
отдельный класс-помощник и переиспользовать ее сколько угодно раз.

"""


class PositiveNumber:
    """Класс дескриптор для положительных чисел."""

    def __set_name__(self, owner, name):
        self.name = '_' + name

    def __get__(self, inst, owner):
        return getattr(inst, self.name, None)

    def __set__(self, inst, value):
        if not isinstance(value, (int, float)):
            raise TypeError('Значение должно быть int или float')
        if value < 0:
            raise ValueError(f"Атрибут '{self.name[1:]}' не может быть отрицательным!")
        setattr(inst, self.name, value)


class Product:
    price = PositiveNumber()
    stock = PositiveNumber()

    def __init__(self, name: str, price: float, stock: int):
        self.name = name
        self.price = price
        self.stock = stock


if __name__ == '__main__':
    item = Product("Рюкзак", 3500.0, 10)
    print(item.price)  # 3500.0

    # Попробуем передать отрицательное количество на склад:
    try:
        item.stock = -5
    except ValueError as e:
        print(f"Ошибка перехвачена: {e}")

