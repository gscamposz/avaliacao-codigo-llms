class DiscountCalculator:
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = cart
        self.promotion = promotion


    def total(self):
        return sum(item['quantity'] * item['price'] for item in self.cart)


    def due(self):
        discount = 0.0
        if self.promotion is not None:
            discount = self.promotion(self)
        return self.total() - discount


    @staticmethod
    def FidelityPromo(order):
        if order.customer['fidelity'] > 1000:
            return order.total() * 0.05
        return 0.0


    @staticmethod
    def BulkItemPromo(order):
        discount = 0.0
        for item in order.cart:
            if item['quantity'] >= 20:
                discount += item['quantity'] * item['price'] * 0.1
        return discount


    @staticmethod
    def LargeOrderPromo(order):
        unique_products = len({item['product'] for item in order.cart})
        if unique_products >= 10:
            return order.total() * 0.07
        return 0.0


customer = {'name': 'Alice', 'fidelity': 1500}
cart = [{'product': 'Laptop', 'quantity': 2, 'price': 1200},
        {'product': 'Phone', 'quantity': 3, 'price': 600}]
promotion = DiscountCalculator.FidelityPromo

order = DiscountCalculator(customer, cart, promotion)
print("Total:", order.total())  # Output: 3600.0
print("Due:", order.due())       # Output: 3420.0 (3600 - 180)
