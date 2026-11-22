
class Order:
    """
    The class manages restaurant orders by allowing the addition of dishes,
    calculation of the total cost, and checkout.
    """

    def __init__(self):
        """
        Initialize the order management system.
        """
        self.menu = []
        self.selected_dishes = []
        self.sales = {}

    def add_dish(self, dish):
        """
        Add a dish to the order if sufficient inventory is available.
        :param dish: dict, containing dish, count, and price.
        :return: bool, True if successfully added, False otherwise.
        """
        dish_name = dish["dish"]
        count = dish["count"]

        if count <= 0:
            return False

        for menu_dish in self.menu:
            if menu_dish["dish"] == dish_name:
                if menu_dish["count"] < count:
                    return False

                menu_dish["count"] -= count

                for selected in self.selected_dishes:
                    if selected["dish"] == dish_name:
                        selected["count"] += count
                        return True

                self.selected_dishes.append({
                    "dish": dish_name,
                    "count": count,
                    "price": menu_dish["price"]
                })

                return True

        return False

    def calculate_total(self):
        """
        Calculate the total cost of ordered dishes,
        applying the sales multiplier when available.
        :return: float, the final total price.
        """
        total = 0.0

        for dish in self.selected_dishes:
            dish_name = dish["dish"]
            count = dish["count"]
            price = dish["price"]

            discount = self.sales.get(dish_name, 1.0)

            total += count * price * discount

        return float(total)

    def checkout(self):
        """
        Check out the ordered dishes.
        :return: False if no dishes are selected,
                 otherwise the total cost.
        """
        if not self.selected_dishes:
            return False

        return self.calculate_total()
