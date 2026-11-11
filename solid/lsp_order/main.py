from order import PhysicalProduct, DigitalProduct


if __name__ == '__main__':
    cart_items = [
        PhysicalProduct(
            name="Кроссовки Nike", price=7500.0, weight=1.2
        ),  # физический
        DigitalProduct(
            name="Курс по Python", price=4000.0
        ),  # цифровой (нет веса и доставки)
        PhysicalProduct(name="Рюкзак", price=3500.0, weight=0.8),  # физический
    ]

    # Общая логика расчета стоимости товаров
    # Она работает со ВСЕМИ товарами одинаково, так как все они — это Product
    total_goods_price = sum(item.name and item.price for item in cart_items)
    print(f"Сумма за товары: {total_goods_price} руб.")


    # Логика расчета доставки
    def calculate_shipping(items: list) -> float:
        total_shipping = 0.0
        for item in items:
            # Мы безопасно проверяем, есть ли у конкретного товара метод доставки.
            # Никаких внезапных NotImplementedError и падений программы!
            if isinstance(item, PhysicalProduct):
                total_shipping += item.get_shipping_cost()
        return total_shipping