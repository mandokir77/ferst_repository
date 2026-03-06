"""
Модуль для управления магазинами сети розничной торговли.
"""

from typing import Optional


class Store:
    """Класс для создания магазинов сети."""

    def __init__(self, name: str, address: str):
        """
        Конструктор магазина.

        Args:
            name: название магазина
            address: адрес магазина
        """
        self.name = name
        self.address = address
        self.items: dict[str, float] = {}

    def add_item(self, product_name: str, price: float) -> None:
        """
        Добавить товар в ассортимент.

        Args:
            product_name: название товара
            price: цена товара
        """
        self.items[product_name] = price

    def remove_item(self, product_name: str) -> bool:
        """
        Удалить товар из ассортимента.

        Args:
            product_name: название товара

        Returns:
            True если товар был удалён, False если товар не найден
        """
        if product_name in self.items:
            del self.items[product_name]
            return True
        return False

    def get_price(self, product_name: str) -> Optional[float]:
        """
        Получить цену товара по названию.

        Args:
            product_name: название товара

        Returns:
            Цена товара или None, если товар отсутствует
        """
        return self.items.get(product_name)

    def update_price(self, product_name: str, new_price: float) -> bool:
        """
        Обновить цену товара.

        Args:
            product_name: название товара
            new_price: новая цена

        Returns:
            True если цена обновлена, False если товар не найден
        """
        if product_name in self.items:
            self.items[product_name] = new_price
            return True
        return False


# Создание нескольких магазинов
if __name__ == "__main__":
    # Магазин 1: Продуктовый
    store1 = Store("Продукты у дома", "ул. Ленина, 15")
    store1.add_item("apples", 0.5)
    store1.add_item("bananas", 0.75)
    store1.add_item("milk", 1.2)
    store1.add_item("bread", 0.9)

    # Магазин 2: Электроника
    store2 = Store("ТехноМир", "пр. Мира, 42")
    store2.add_item("laptop", 899.99)
    store2.add_item("smartphone", 499.99)
    store2.add_item("headphones", 79.99)

    # Магазин 3: Одежда
    store3 = Store("Стиль", "ул. Центральная, 7")
    store3.add_item("t-shirt", 19.99)
    store3.add_item("jeans", 49.99)
    store3.add_item("jacket", 89.99)

    # Демонстрация работы методов
    print(f"Магазин: {store1.name}, Адрес: {store1.address}")
    print(f"Цена яблок: {store1.get_price('apples')}")
    print(f"Цена несуществующего товара: {store1.get_price('oranges')}")
    store1.update_price("bread", 1.0)
    print(f"Новая цена хлеба: {store1.get_price('bread')}")
    print()
