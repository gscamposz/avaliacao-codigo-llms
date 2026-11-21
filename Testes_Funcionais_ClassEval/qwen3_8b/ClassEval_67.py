class Order:
    def __init__(self):
        """
        Initialize an Order with:
        - `menu`: List of available items (each item is a dictionary)
        - `selected_dishes`: List of items in the cart (each item is a dictionary)
        - `sales`: Dictionary to apply discounts per item
        """
        self.menu = []
        self.selected_dishes = []
        self.sales = {}

    def add_dish(self, dish):
        """
        Add a specified quantity of a dish to the cart.

        Parameters:
        - `dish`: A dictionary with keys 'dish', 'count', and 'price'
        """
        for item in self.menu:
            if item['dish'] == dish['dish']:
                if dish['count'] <= item['count']:
                    selected_dish = {
                        'dish': dish['dish'],
                        'count': dish['count'],
                        'price': item['price']
                    }
                    self.selected_dishes.append(selected_dish)
                    item['count'] -= dish['count']
                    return True
        return False

    def calculate_total(self):
        """
        Calculate the total price of the selected dishes,
        applying any discounts from the `sales` dictionary.

        Returns:
        - Total price as a float
        """
        total = 0.0
        for dish in self.selected_dishes:
            dish_name = dish['dish']
            count = dish['count']
            price = dish['price']
            discount = self.sales.get(dish_name, 1.0)
            total += count * price * discount
        return total

    def checkout(self):
        """
        Finalize the order by calculating the total.

        Returns:
        - Total price of the order
        """
        if not self.selected_dishes:
            return False
        return self.calculate_total()


# Create an Order instance
order = Order()

# Add items to the menu
order.menu.append({"dish": "dish1", "price": 10, "count": 5})
order.menu.append({"dish": "dish2", "price": 15, "count": 3})

# Add items to the cart
order.add_dish({"dish": "dish1", "count": 3})  # Adds 3 units of dish1
order.add_dish({"dish": "dish2", "count": 2})  # Adds 2 units of dish2

# Set sales (discounts)
order.sales = {"dish1": 0.8, "dish2": 0.9}

# Calculate and print the total
total = order.checkout()
print(f"Total price: ${total:.2f}")
