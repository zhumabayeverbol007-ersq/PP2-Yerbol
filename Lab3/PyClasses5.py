class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
    
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited ${amount}. New balance: ${self.balance}")
        else:
            print("Deposit amount must be positive")
    
    def withdraw(self, amount):
        if amount > self.balance:
            print(f"Insufficient funds! Available: ${self.balance}")
        elif amount <= 0:
            print("Withdrawal amount must be positive")
        else:
            self.balance -= amount
            print(f"Withdrew ${amount}. New balance: ${self.balance}")
    
    def __str__(self):
        return f"Account owner: {self.owner}\nAccount balance: ${self.balance}"

acc = Account("Temirlan Anarbekov", 25000)
print(acc)

acc.deposit(5000)    # Deposited $5000. New balance: $30000
acc.withdraw(2000)   # Withdrew $2000. New balance: $28000
acc.withdraw(35000)  # Insufficient funds! Available: $28000
acc.deposit(-100)   # Deposit amount must be positive