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
            cur.execute('SELECT pin, balance FROM card WHERE number=?', [user_card_number])
            try:
                pin, balance = cur.fetchone()
            except:
                print("\nWrong card number or PIN!\n")
                continue
            if user_pin == pin:
                print("\nYou have successfully logged in!\n")
                exit_program = False

                # SUBMENU
                while True:
                    print("1. Balance")
                    print("2. Log out")
                    print("0. Exit")
                    client_input = input()
                    if client_input == '1':
                        print("Balance:", balance)
                    elif client_input == '2':
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
