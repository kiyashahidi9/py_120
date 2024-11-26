class InvoiceEntry:
    def __init__(self, product_name, number_purchased):
        self._product_name = product_name
        self.quantity = number_purchased

    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self, num):
        if not isinstance(num, int):
            raise TypeError('Only numbers plz <3')

        self._quantity = num

entry = InvoiceEntry('Marbles', 5000)
print(entry.quantity)         # 5000

entry.quantity = 10_000
print(entry.quantity)         # 10_000