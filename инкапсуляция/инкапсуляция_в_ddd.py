"""

class Product:

    def __init__(self, name: str, price: float, stock: int):
        self.name = name
        # Сразу используем сеттеры для валидации при создании
        self.price = price -> value_object
        self.stock = stock -> value_object

"""

# 1. Создаем Value Object для цены
class Money:

    def __init__(self, amount: float):
        if amount <= 0:
            raise ValueError("Сумма должна быть больше нуля")
        self._amount = float(amount)

    @property
    def amount(self) -> float:
        return self._amount

    def __repr__(self):
        return f"{self._amount} руб."


# 2. Создаем Value Object для количества
class Quantity:

    def __init__(self, value: int):
        if value < 0:
            raise ValueError("Количество не может быть отрицательным")
        self._value = int(value)

    @property
    def value(self) -> int:
        return self._value


# 3. Доменная модель использует эти объекты
class Product:

    def __init__(self, name: str, price: Money, stock: Quantity):
        self.name = name
        self.price = price  # Здесь уже гарантированно валидный объект Money
        self.stock = stock  # Здесь гарантированно валидный Quantity


"""
если атрибут неизменяемый, то можно делать прямой доступ

Для коллекций (списков, словарей) правила инкапсуляции работают совершенно по-другому, 
потому что коллекция — это составная структура данных, и здесь мы имеем дело с 
понятием Агрегата (Aggregate Root) в DDD.

Если объект содержит внутри себя список других объектов (например, Order содержит список товаров OrderItem), действуют жесткие архитектурные правила:

1) Никакого прямого доступа на запись. Мы никогда не даем наружу метод вроде order.items.append(...).
2) Только чтение через неизменяемый срез (Read-Only View). Наружу мы отдаем коллекцию в виде кортежа (tuple) или итератора, чтобы внешний код мог посмотреть список товаров (например, для отрисовки в корзине), но не мог его сломать.
3) Управление изменениями — только через методы агрегата. Все добавления, удаления и изменения происходят строго через методы класса-владельца (add_item, remove_item), который контролирует бизнес-правила.
"""


class OrderItem:
    # Элемент заказа — это Value Object (лучше сделать его неизменяемым)
    def __init__(self, product_name: str, price: float, quantity: int):
        if quantity <= 0:
            raise ValueError("Количество должно быть больше нуля")
        self.product_name = product_name
        self.price = price
        self.quantity = quantity


class Order:
    def __init__(self, customer_email: str):
        self.customer_email = customer_email
        self._items: list[OrderItem] = []  # Приватный список, скрыт от внешнего мира

    # Геттер возвращает ТУПЛ (неизменяемый срез)
    @property
    def items(self) -> tuple[OrderItem, ...]:
        return tuple(self._items)

    # Управляем коллекцией строго через методы с валидацией
    def add_item(self, product_name: str, price: float, quantity: int):
        # Бизнес-правило: проверяем, нет ли уже такого товара в заказе
        for item in self._items:
            if item.product_name == product_name:
                item.quantity += quantity
                return

        # Если товара нет, создаем элемент и добавляем
        new_item = OrderItem(product_name, price, quantity)
        self._items.append(new_item)

    def remove_item(self, product_name: str):
        # Пересоздаем список без удаляемого товара
        self._items = [item for item in self._items if item.product_name != product_name]

    def get_total(self) -> float:
        return sum(item.price * item.quantity for item in self._items)


class Product:

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price
        # Приватный список для хранения тегов
        self._tags: list[str] = []

    # Геттер возвращает неизменяемый срез (tuple), чтобы теги нельзя было изменить снаружи
    @property
    def tags(self) -> tuple[str, ...]:
        return tuple(self._tags)

    # Управляем коллекцией тегов через контролируемые методы
    def add_tag(self, tag: str):
        cleaned_tag = tag.strip().lower()
        if not cleaned_tag:
            raise ValueError("Тег не может быть пустым")

        if cleaned_tag not in self._tags:
            self._tags.append(cleaned_tag)

    def remove_tag(self, tag: str):
        cleaned_tag = tag.strip().lower()
        if cleaned_tag in self._tags:
            self._tags.remove(cleaned_tag)


"""
Если внутри твоей доменной модели вместо примитивного списка появляется другой класс, который содержит внутри себя словарь (dict), правила игры становятся еще интереснее.

Словарь в Python — это изменяемый объект (mutable). Если отдать на него прямую ссылку, инкапсуляция мгновенно рухнет.

Давай разберем, как правильно поступать, если у Product есть вложенный объект (например, ProductSpecifications или Metadata), который управляет словарем характеристик (вроде {"color": "red", "size": "XL"}).
"""

from types import MappingProxyType

class ProductSpecifications:
    def __init__(self, initial_specs: dict[str, str] = None):
        # При инициализации создаем копию словаря, чтобы защититься от внешних мутаций
        self._data: dict[str, str] = dict(initial_specs) if initial_specs else {}

    @property
    def raw_data(self) -> dict[str, str]:
        # 🛡️ Возвращаем неизменяемую обертку (MappingProxyType).
        # Внешний код сможет ЧИТАТЬ словарь, но не сможет в него ничего записать или удалить!
        return MappingProxyType(self._data)

    # Контролируемые методы для изменения состояния внутри объекта
    def set_spec(self, key: str, value: str):
        if not key.strip():
            raise ValueError("Ключ характеристики не может быть пустым")
        self._data[key] = value

    def remove_spec(self, key: str):
        if key in self._data:
            del self._data[key]


class Product:
    def __init__(self, name: str, price: float, specs: ProductSpecifications):
        self.name = name
        self.price = price
        self._specs = specs  # Храним вложенный объект инкапсулированно

    @property
    def specs(self) -> ProductSpecifications:
        # Возвращаем сам объект характеристик.
        # Так как он спроектирован как защищенный Value Object, это безопасно.
        return self._specs


"""
Резюме для вложенных объектов со словарями:

1) Не отдавай dict наружу напрямую. Если вернуть обычный self._dict, его изменят через .update() или .pop() в обход бизнес-логики.
2) Используй MappingProxyType, если нужно дать возможность читать словарь снаружи без права записи.
3) Управляй изменениями через методы вложенного объекта (set_spec, remove_spec), чтобы сохранять контроль над инвариантами.
"""