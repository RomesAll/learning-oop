"""
Определение: Создавайте узкие интерфейсы, ориентированные на конкретного клиента. Клиенты не должны зависеть от методов,
которые они не используют.
Простыми словами: Лучше сделать много маленьких и специализированных интерфейсов (абстрактных классов), чем один толстый
универсальный интерфейс, методы которого дочерним классам приходится заглушать или оставлять пустыми.
"""

"""
Пример нарушения

class Worker(ABC):

    @abstractmethod
    def manage_inventory(self):
        pass

    @abstractmethod
    def update_product_catalog(self):
        pass

    @abstractmethod
    def handle_support_tickets(self):
        pass


# 1. Кладовщик должен управлять только складом
class WarehouseWorker(Worker):

    def manage_inventory(self):
        print("Обновление остатков на складе...")

    def update_product_catalog(self):
        # Ему это не нужно! Но интерфейс заставляет реализовать метод.
        raise NotImplementedError("Кладовщик не редактирует каталог!")

    def handle_support_tickets(self):
        # Тоже не его зона ответственности!
        raise NotImplementedError("Кладовщик не отвечает в поддержке!")
"""

from abc import ABC, abstractmethod


# 1. Узкие интерфейсы под конкретные задачи
class InventoryManager(ABC):

    @abstractmethod
    def manage_inventory(self):
        pass


class CatalogManager(ABC):

    @abstractmethod
    def update_product_catalog(self):
        pass


class SupportAgent(ABC):

    @abstractmethod
    def handle_support_tickets(self):
        pass


# 2. Кладовщик реализует только то, с чем работает
class WarehouseWorker(InventoryManager):

    def manage_inventory(self):
        print("Обновление остатков на складе...")


# 3. Контент-менеджер отвечает только за каталог
class ContentManager(CatalogManager):

    def update_product_catalog(self):
        print("Добавление новых товаров и описаний...")