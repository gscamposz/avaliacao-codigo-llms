class VendingMachine:
    """
    This is a class to simulate a vending machine, including adding products, inserting coins, purchasing products, viewing balance, replenishing product inventory, and displaying product information.
    """

    def __init__(self):
        """
        Initializes the vending machine's inventory and balance.
        """
        self.inventory = {}
        self.balance = 0

    def add_item(self, item_name, price, quantity):
        """
        Adds a product to the vending machine's inventory.
        """
        self.inventory[item_name] = {
            'price': price,
            'quantity': quantity
        }

    def insert_coin(self, amount):
        """
        Inserts coins into the vending machine and returns the balance.
        """
        self.balance += amount
        return self.balance

    def purchase_item(self, item_name):
        """
        Purchases a product and returns the remaining balance.
        Returns False if the purchase is unsuccessful.
        """
        if item_name not in self.inventory:
            return False

        item = self.inventory[item_name]

        if item['quantity'] <= 0:
            print("Purchase unsuccessful")
            return False

        if self.balance < item['price']:
            return False

        self.balance -= item['price']
        item['quantity'] -= 1

        return self.balance

    def restock_item(self, item_name, quantity):
        """
        Replenishes the inventory of an existing product.
        """
        if item_name not in self.inventory:
            return False

        self.inventory[item_name]['quantity'] += quantity
        return True

    def display_items(self):
        """
        Returns a formatted string containing the available products.
        Returns False if the inventory is empty.
        """
        if not self.inventory:
            return False

        return '\n'.join(
            f"{name} - ${item['price']} [{item['quantity']}]"
            for name, item in self.inventory.items()
        )