from abc import abstractmethod, ABC


class DiscountCalculation(ABC):
    """Абстрактный класс для подсчета скидок."""

    @abstractmethod
    def apply(self, total: float) -> float:
        ...


class RegularDiscount(DiscountCalculation):
    def apply(self, total: float) -> float:
        return total * 0.95


class VipDiscount(DiscountCalculation):
    def apply(self, total: float) -> float:
        return total * 0.80