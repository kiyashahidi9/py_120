class Customer:

    def place_order(self):
        self.order = Order()

class Order:

    def __init__(self):
        self.burger = Burger()
        self.side = Side()
        self.drink = Drink()

    def total(self):
        total_cost = self.burger + self.side + self.drink
        # :.2f formats the price as needed
        return f'${total_cost:.2f}'

def meal(self):
    return [self.burger, self.side, self.drink]

class MealItem:
    pass

class Burger(MealItem):
    OPTIONS = {
        '1': { 'name': 'LS Burger', 'cost': 3.00 },
        '2': { 'name': 'LS Cheeseburger', 'cost': 3.50 },
        '3': { 'name': 'LS Chicken Burger', 'cost': 4.50 },
        '4': { 'name': 'LS Double Deluxe Burger', 'cost': 6.00 }
    }

class Side(MealItem):
    OPTIONS = {
        '1': { 'name': 'Fries', 'cost': 0.99 },
        '2': { 'name': 'Onion Rings', 'cost': 1.50 }
    }

class Drink(MealItem):
    OPTIONS = {
        '1': { 'name': 'Cola', 'cost': 1.50 },
        '2': { 'name': 'Lemonade', 'cost': 1.50 },
        '3': { 'name': 'Vanilla Shake', 'cost': 2.00 },
        '4': { 'name': 'Chocolate Shake', 'cost': 2.00 },
        '5': { 'name': 'Strawberry Shake', 'cost': 2.00 }
    }