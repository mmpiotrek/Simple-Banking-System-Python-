# Write your code here
import random
import sqlite3


class Account:
    def __init__(self, last_id):
        self.mii = '4'
        self.iin = '00000'
        random.seed(last_id)
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


def luhn_algorithm(card_number):
    digits = []
    for i, digit in enumerate(list(map(int, [*card_number[:-1]]))):
        if i % 2 == 0:
            digit *= 2
            if digit > 9:
                digit -= 9
        digits.append(digit)
    checksum = 10 - sum(digits) % 10
    if checksum == 10:
        checksum = 0
    if checksum == int(card_number[-1]):
        return True
    else:
        return False


if __name__ == '__main__':
    conn = sqlite3.connect('./card.s3db')
    cur = conn.cursor()
    try:
        cur.execute("CREATE TABLE card ("
                    "id INTEGER,"
                    "number TEXT,"
                    "pin TEXT,"
                    "balance INTEGER DEFAULT 0)")
    except:
        pass
    conn.commit()
    while True:
        # MENU
        print("1. Create an account")
        print("2. Log into account")
        print("0. Exit")
        user_input = input()
        if user_input == '1':
            cur.execute('SELECT MAX(id) FROM card')
            last_card_id = cur.fetchone()[0]
            if not last_card_id:
                last_card_id = 0
            account = Account(last_card_id)
            next_id = last_card_id + 1

            cur.execute('INSERT INTO card VALUES (?,?,?,?)', [
                next_id,
                account.card_number,
                account.pin,
                account.balance
            ])
            conn.commit()

            print("\nYour card has been created")
            print("Your card number:")
            print(account.card_number)
            print("Your card PIN:")
            print(f"{account.pin}\n")

        elif user_input == '2':
            user_card_number = input("Enter your card number:\n")
            user_pin = input("Enter your PIN:\n")
            cur.execute('SELECT pin '
                        'FROM card '
                        'WHERE number=?', [user_card_number])
            try:
                pin = cur.fetchone()[0]
            except:
                print("\nWrong card number or PIN!\n")
                continue
            if user_pin == pin:
                print("\nYou have successfully logged in!\n")
                exit_program = False

                # SUBMENU for account
                while True:
                    print("1. Balance")
                    print("2. Add income")
                    print("3. Do transfer")
                    print("4. Close account")
                    print("5. Log out")
                    print("0. Exit")
                    client_input = input()
                    cur.execute('SELECT balance '
                                'FROM card '
                                'WHERE number=?', [user_card_number])
                    balance = cur.fetchone()
                    if balance is not None:
                        balance = balance[0]

                    if client_input == '1':
                        print("Balance:", balance)
                    elif client_input == '2':
                        income = int(input("Enter income:"))
                        request = f"UPDATE card SET balance={income+balance} WHERE number='{user_card_number}' AND pin='{user_pin}'"
                        conn.execute(request)
                        conn.commit()
                        print("Income was added")
                    elif client_input == '3':
                        print("Transfer")
                        transfer_card_number = input("Enter card number:")
                        luhn_condition = luhn_algorithm(transfer_card_number)
                        if not luhn_condition:
                            print("Probably you made a mistake in the card number. Please try again!")
                            continue
                        if transfer_card_number == user_card_number:
                            print("You can't transfer money to the same account!")
                        try:
                            cur.execute('SELECT number '
                                        'FROM card '
                                        'WHERE number=?', [transfer_card_number])
                        except:
                            print("\nSuch a card does not exist.\n")
                            continue
                        if cur.fetchone() is None:
                            print("\nSuch a card does not exist.\n")
                            continue
                        transfer_money = int(input("Enter how much money you want to transfer:"))
                        if transfer_money > balance:
                            print("Not enough money!")
                            continue
                        else:
                            cur.execute('SELECT balance '
                                        'FROM card '
                                        'WHERE number=?', [transfer_card_number])
                            transfer_balance = cur.fetchone()[0]
                            request = f"UPDATE card SET balance={balance-transfer_money} WHERE number='{user_card_number}' AND pin='{user_pin}'"
                            conn.execute(request)
                            conn.commit()
                            request = f"UPDATE card SET balance={transfer_balance+transfer_money} WHERE number='{transfer_card_number}'"
                            conn.execute(request)
                            conn.commit()
                            print("Success!")
                    elif client_input == '4':
                        request = f"DELETE FROM card WHERE number='{user_card_number}'"
                        cur.execute(request)
                        conn.commit()
                        print("The account has been closed!")
                        break
                    elif client_input == '5':
                        print("\nYou have successfully logged out!\n")
                        break
                    elif client_input == '0':
                        exit_program = True
                        break
                    else:
                        print()
                if exit_program:
                    break
            else:
                print("\nWrong card number or PIN!\n")

        elif user_input == '0':
            break
        else:
            print()
    conn.close()
    print("Bye!")
