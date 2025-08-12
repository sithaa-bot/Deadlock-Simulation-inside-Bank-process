import threading
import time


class BankAccount:
    """
    Represents a bank account with a balance, a name, and a lock for thread safety.
    """
    def __init__(self, name: str, initial_balance: float):
        self.name = name
        self.balance = initial_balance
        self.lock = threading.Lock()

    def withdraw(self, amount: float):
        """Withdraws a specified amount from the account."""
        if self.balance >= amount:
            self.balance -= amount
            print(f"[{self.name}]  Withdrawn: ${amount:.2f} | New Balance: ${self.balance:.2f}")
        else:
            print(f"[{self.name}]  Withdrawal of ${amount:.2f} failed (Insufficient funds)")

    def deposit(self, amount: float):
        """Deposits a specified amount into the account."""
        self.balance += amount
        print(f"[{self.name}]  Deposited: ${amount:.2f} | New Balance: ${self.balance:.2f}")

    def get_balance(self) -> float:
        """Returns the current balance of the account."""
        return self.balance

    def get_name(self) -> str:
        """Returns the name of the account."""
        return self.name


def transfer(from_account: BankAccount, to_account: BankAccount, amount: float):
    """
    Transfers money from one account to another (thread-safe).
    """
    thread_name = threading.current_thread().name
    print(f" {thread_name} is transferring ${amount:.2f} from {from_account.get_name()} to {to_account.get_name()}")

    with from_account.lock:
        time.sleep(0.1)  # Simulate processing delay
        from_account.withdraw(amount)

    with to_account.lock:
        time.sleep(0.1)  # Simulate processing delay
        to_account.deposit(amount)

    print(f" {thread_name} transfer complete!")


def simple_withdraw(account: BankAccount, amount: float):
    """Withdraw money from a single account (thread-safe)."""
    thread_name = threading.current_thread().name
    print(f" {thread_name} is withdrawing ${amount:.2f} from {account.get_name()}")

    with account.lock:
        time.sleep(0.1)  # Simulate processing delay
        account.withdraw(amount)

    print(f" {thread_name} withdrawal complete!")


def main():
    """Main function to run the deposit-then-withdraw sequence."""
    print("\n --- Deposit then Withdraw Simulation ---\n")

    # Create two bank accounts
    account_a = BankAccount("Account-A", 1000)
    account_b = BankAccount("Account-B", 500)

    print(f" Initial Balances:")
    print(f"   {account_a.get_name()}: ${account_a.get_balance():.2f}")
    print(f"   {account_b.get_name()}: ${account_b.get_balance():.2f}\n")

    # Step 1: Deposit from A to B
    thread1 = threading.Thread(
        target=transfer,
        args=(account_a, account_b, 200),
        name="Deposit-Thread (A → B)"
    )

    # Step 2: Withdraw from B
    thread2 = threading.Thread(
        target=simple_withdraw,
        args=(account_b, 150),
        name="Withdraw-Thread (B)"
    )

    # Start deposit first, then withdraw
    thread1.start()
    thread1.join()

    thread2.start()
    thread2.join()

    print("\n Final Balances:")
    print(f"   {account_a.get_name()}: ${account_a.get_balance():.2f}")
    print(f"   {account_b.get_name()}: ${account_b.get_balance():.2f}")
    print("\n Simulation Finished Successfully!\n")


if __name__ == "__main__":
    main()
