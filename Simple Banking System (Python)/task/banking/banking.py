# Write your code here
import random


class Account:
    def __init__(self, other_accounts):
        self.mii = '4'
        self.iin = '00000'
        random.seed(len(other_accounts))
        self.customer_account = "{:09d}".format(random.randint(0, 999_999_999))
        self.bin = ''.join([str(self.mii),
                            str(self.iin),
                            self.customer_account])
        digits = []
        for i, digit in enumerate(list(map(int, [*self.bin]))):
            if i % 2 == 0:
                digit *= 2
                if digit > 9:
                    digit -= 9
            digits.append(digit)
        self.checksum = 10 - sum(digits) % 10
        self.card_number = ''.join([str(self.bin), str(self.checksum)[-1]])
        self.pin = "{:04d}".format(random.randint(0, 9999))
        self.balance = 0

    def account_menu(self):
        while True:
            print("1. Balance")
            print("2. Log out")
            print("0. Exit")
            client_input = input()
            if client_input == '1':
                print("Balance:", self.balance)
            elif client_input == '2':
                print("\nYou have successfully logged out!\n")
                return False
            elif client_input == '0':
                return True
            else:
                print()


if __name__ == '__main__':
    accounts = {}
    while True:
        # MENU
        print("1. Create an account")
        print("2. Log into account")
        print("0. Exit")
        user_input = input()
        if user_input == '1':
            account = Account(accounts)
            accounts[account.card_number] = account

            print("\nYour card has been created")
            print("Your card number:")
            print(account.card_number)
            print("Your card PIN:")
            print(f"{account.pin}\n")

        elif user_input == '2':
            user_card_number = input("Enter your card number:\n")
            user_pin = input("Enter your PIN:\n")
            if user_card_number in accounts and user_pin == accounts[user_card_number].pin:
                print("\nYou have successfully logged in!\n")
                exit_request = accounts[user_card_number].account_menu()
                if exit_request:
                    break
            else:
                print("\nWrong card number or PIN!\n")

        elif user_input == '0':
            break
        else:
            print()
    print("Bye!")
