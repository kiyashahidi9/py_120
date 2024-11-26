class BankAccount:
    def __init__(self, starting_balance):
        self._balance = starting_balance

    def balance_is_positive(self):
        return self.balance > 0

    @property
    def balance(self):
        return self._balance
    
'''
Alyssa is correct, since the `self.balance` is referring to the balance property that 
she has defined, which returns the starting balance.
'''