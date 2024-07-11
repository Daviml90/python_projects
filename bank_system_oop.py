from abc import ABC, abstractmethod

class Account:

    def __init__(self, balance, number, routing, client):
        self._balance = balance
        self._number = number
        self._routing = routing
        self._client = client
        self._history = History()

    def see_balance(self):
        print(self._balance)
    
    def create_new_account(self):
        self._client.add_account()

    def withdraw(self, ammount):
        if self._balance < ammount:
            print("Insufficient balance.")
            return False
        else:
            transaction = Withdraw(ammount)
            self._balance -= ammount
            self._history.add_transaction(transaction)

    def deposit(self, ammount):      
        transaction = Deposit(ammount)
        self._balance += ammount
        self._history.add_transaction(transaction)
    
    def print_history(self):
        for transaction in self._history._history:
            transaction.register(self)
        print(f"Balance = {self._balance}")

class Natural_Person:
    def __init__(self,ssn, name, birthday):
        self._ssn = ssn
        self._name = name
        self._birthday = birthday

class Client(Natural_Person):
    def __init__(self, address, accounts=[Account]):
        self._address = address
        self._accounts = [accounts]

    def make_deposit(self, account: Account, ammount):
        account.deposit(ammount)

    def make_withdraw(self, account: Account, ammount):
        account.withdraw(ammount)

    def add_account(self, account =Account):
        self._accounts.append(account)

class Checking_Account(Account):
    def __init__(self, balance, number, routing, client, limit=500, withdraws_per_day=3):
        super().__init__(balance, number, routing, client)
        self.limit = limit
        self.withdraw_per_day = withdraws_per_day


    def withdraw(self, ammount):
        num_withdraws = len(
            [transaction for transaction in self._history._history if transaction.__name__ == "Withdraw"]
        )


        if ammount <= self.limit and num_withdraws < self.withdraw_per_day:
            super().withdraw(ammount)
            return True
        else:
            print("Exceeded limit.")
            return False

class Transaction(ABC):
    @abstractmethod
    def register(self, account=Account):
        pass

class Deposit(Transaction):
    def __init__(self, ammount):
        self._ammount = ammount
    def register(self, account=Account):
        print(f"Account: {account._number} \t (+) {self._ammount}")

class Withdraw(Transaction):
    def __init__(self, ammount):
        self._ammount = ammount
    def register(self, account=Account):
        print(f"Account: {account._number} \t (-) {self._ammount}")

class History:
    _history = [Transaction]
    def add_transaction(self, transaction=Transaction):
        self._history.append(transaction)
    




# Testing

client = Client("Brazil")

checking_account = Checking_Account(100,"1234","001",client)

checking_account.withdraw(200)
checking_account.deposit(400)

checking_account.print_history()


                    



