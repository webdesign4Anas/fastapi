def add(x:int,y:int):
    return x+y


class Insuffiecent(Exception):
    pass
class Bank():



    def __init__(self,starting_balance=0):
        self.balance=starting_balance

    def deposit(self,amount):
        self.balance+=amount

    def withdraw(self,amount):
        if amount>self.balance:
            raise  Insuffiecent("insufficient funds")
        self.balance-=amount        