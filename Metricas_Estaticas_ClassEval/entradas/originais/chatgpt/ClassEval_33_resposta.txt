
class DiscountStrategy:
    """
    This is a class that allows to use different discount strategy
    based on shopping credit or shopping cart in supermarket.
    """

    def __init__(self, customer, cart, promotion=None):
        """
        Initialize the DiscountStrategy with customer information,
        a cart of items, and an optional promotion.
        """
        self.customer = customer
        self.cart = cart
        self.promotion = promotion
        self.total()

    def total(self):
        """
        Calculate the total cost of items in the cart.
        :return: float, total cost of items
        """
        return float(sum(
            item['quantity'] * item['price']
            for item in self.cart
        ))

    def due(self):
        """
        Calculate the final amount to be paid after applying
        the discount.
        :return: float, final amount to be paid
        """
        discount = self.promotion(self) if self.promotion else 0
        return float(self.total() - discount)

    @staticmethod
    def FidelityPromo(order):
        """
        Customers with over 1000 fidelity points receive
        a 5% discount on the entire order.
        :return: float, discount amount
        """
        if order.customer.get('fidelity', 0) > 1000:
            return float(order.total() * 0.05)
        return 0.0

    @staticmethod
    def BulkItemPromo(order):
        """
        Items with a quantity of 20 or more receive
        a 10% discount.
        :return: float, discount amount
        """
        discount = sum(
            item['quantity'] * item['price'] * 0.10
            for item in order.cart
            if item['quantity'] >= 20
        )
        return float(discount)

    @staticmethod
    def LargeOrderPromo(order):
        """
        Orders containing 10 or more different products
        receive a 7% discount on the entire order.
        :return: float, discount amount
        """
        different_products = {
            item['product'] for item in order.cart
        }

        if len(different_products) >= 10:
            return float(order.total() * 0.07)
        return 0.0
