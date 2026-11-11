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


class NumberValidator:

    def __init__(self, min_value=None, max_value=None):
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(self, owner, name):
        # Автоматически получаем имя атрибута (например, 'price' -> '_price')
        self.name = "_" + name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name, None)

    def __set__(self, instance, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"Атрибут '{self.name[1:]}' должен быть числом!")

        # Проверяем минимальный порог, если он задан
        if self.min_value is not None and value < self.min_value:
            raise ValueError(
                f"Значение '{self.name[1:]}' ({value}) не может быть меньше {self.min_value}!"
            )

        # Проверяем максимальный порог, если он задан
        if self.max_value is not None and value > self.max_value:
            raise ValueError(
                f"Значение '{self.name[1:]}' ({value}) не может быть больше {self.max_value}!"
            )

        setattr(instance, self.name, value)


class Product:
    price = NumberValidator(min_value=0.01)
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

    try:
        item.price = 0
    except ValueError as e:
        print(f"Ошибка цены: {e}")

