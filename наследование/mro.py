"""
MRO — это строго линейный порядок обхода классов при поиске методов и атрибутов,
который выстраивается по алгоритму C3.

MRO (Method Resolution Order — порядок разрешения методов) — это важнейший механизм в Python,
определяющий порядок, в котором интерпретатор ищет методы и атрибуты в иерархии классов.
Это особенно критично при множественном наследовании.
"""

class LoggerMixin:
    def process(self):
        print("Логируем действие...")
        super().process()  # Вызовет следующий класс в MRO!

class Authenticator:
    def process(self):
        print("Проверяем авторизацию...")

class Service(LoggerMixin, Authenticator):
    def process(self):
        print("Запуск основного сервиса бизнес-логики")
        super().process()

# Создаем объект и запускаем метод
s = Service()
s.process()
print(Service.mro())