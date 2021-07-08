import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS card (
                id INTEGER PRIMARY KEY,
                number TEXT,
                pin TEXT,
                balance INTEGER DEFAULT 0
                );""")


class Card:
    all_cards = []

    def __init__(self, card_number, card_pin, card_balance=0):
        self.card_number = card_number
        self.card_pin = card_pin
        self.card_balance = card_balance

    def create_card(self):
        # Generate new card number
        rand_acc_id = random.randint(0, 999999999)
        acc_id = "400000" + f'{rand_acc_id:09}'
        luhn_var = 0
        for i, d in enumerate(acc_id):
            if i % 2 != 0:
                luhn_var = int(luhn_var) + int(d)
            elif i % 2 == 0 and int(d) <= 4:
                luhn_var = int(luhn_var) + int(d) * 2
            elif i % 2 == 0 and int(d) >= 5:
                luhn_var = int(luhn_var) + (int(d) * 2) - 9

        if luhn_var % 10 == 0:
            self.card_number = acc_id + "0"
        elif luhn_var % 10 > 0:
            self.card_number = acc_id + str(10 - (luhn_var % 10))

        # Generate new PIN
        self.card_pin = random.randint(1000, 9999)

        # Adding card to table
        cur.execute("""INSERT INTO card (number, pin) 
                       VALUES (:card_number, :card_pin)""",
                    {'card_number': self.card_number, 'card_pin': self.card_pin}
                    )
        conn.commit()


print(
    "1. Create an account\n"
    "2. Log into account\n"
    "0. Exit\n"
)

while True:
    menu_select = int(input("Please select\n>"))

    if menu_select == 1:  # Create card
        new_card = Card(0, 0)
        new_card.create_card()
        print("Your card has been created\n"
              "\nYour card number:", )
        print(int(new_card.card_number))
        print("Your card PIN:")
        print(int(new_card.card_pin))
        print("\n1. Create an account\n"
              "2. Log into account\n"
              "0. Exit\n")

    if menu_select == 2:  # Log in
        your_card_number = int(input("Enter your card number:\n>"))
        your_pin = int(input("Enter your PIN:\n>"))
        cur.execute('SELECT number, pin FROM card WHERE number = :number AND pin = :pin',
                    {'number': your_card_number, 'pin': your_pin})
        all_cards = cur.fetchall()

        # Log in Successful
        if len(all_cards) == 1:
            print("You have successfully logged in!\n"
                  "\n1. Balance\n"
                  "2. Add income\n"
                  "3. Do transfer\n"
                  "4. Close account\n"
                  "5. Log out\n"
                  "0. Exit")
            while True:
                acc_menu_select = int(input('>'))
                # Ask Balance
                if acc_menu_select == 1:
                    cur.execute('SELECT balance FROM card WHERE number = :number AND pin = :pin',
                                {'number': your_card_number, 'pin': your_pin})
                    conn.commit()
                    balance = cur.fetchall()

                    print("\nBalance:", balance[0][0],
                          "\n\n1. 11Balance\n"
                          "2. Add income\n"
                          "3. Do transfer\n"
                          "4. Close account\n"
                          "5. Log out\n"
                          "0. Exit")
                # Add income
                if acc_menu_select == 2:
                    income = int(input("Enter income:\n>"))
                    cur.execute("UPDATE card SET balance = balance + :balance WHERE number = :number;",
                                {'balance': income, 'number': your_card_number})
                    conn.commit()
                    cur.execute('SELECT balance FROM card WHERE number = :number AND pin = :pin',
                                {'number': your_card_number, 'pin': your_pin})
                    balance = cur.fetchall()

                    print("Income was added!\n",
                          "\n1. 221Balance\n"
                          "2. Add income\n"
                          "3. Do transfer\n"
                          "4. Close account\n"
                          "5. Log out\n"
                          "0. Exit")
                # Do transfer
                if acc_menu_select == 3:
                    transfer_card = int(input("Enter card number:\n>"))
                    cur.execute("SELECT number FROM card WHERE number = :transfer_card;",
                                {'transfer_card': transfer_card})
                    conn.commit()
                    transfer_card_number = cur.fetchall()

                    # Check Luhn algorithm
                    add_all = 0
                    for index, digit in enumerate(str(transfer_card)):
                        if index % 2 != 0:
                            add_all = int(add_all) + int(digit)
                        elif index % 2 == 0 and int(digit) <= 4:
                            add_all = int(add_all) + int(digit) * 2
                        elif index % 2 == 0 and int(digit) >= 5:
                            add_all = int(add_all) + (int(digit) * 2) - 9

                    # Pass Luhn algorithm, card exist
                    if add_all % 10 == 0 and len(transfer_card_number) == 1:
                        transferred_amount = int(input("Enter how much money you want to transfer:\n>"))
                        cur.execute("SELECT balance FROM card WHERE number = :number AND pin = :pin",
                                    {'number': your_card_number, 'pin': your_pin})
                        conn.commit()
                        balance = cur.fetchall()

                        # Success
                        if transferred_amount <= balance[0][0]:
                            cur.execute("UPDATE card SET balance = :transferred_amount WHERE number = :transfer_card;",
                                        {'transferred_amount': transferred_amount, 'transfer_card': transfer_card})
                            cur.execute("UPDATE card SET balance = balance - :transferred_amount WHERE number = :your_card;",
                                        {'transferred_amount': transferred_amount, 'your_card': your_card_number})
                            conn.commit()
                            print("Success!")
                        # Not enough!
                        if transferred_amount > balance[0][0]:
                            print("Not enough money!")

                    # No card!
                    elif add_all % 10 == 0 and len(transfer_card_number) == 0:
                        print("Such a card does not exist.")

                    # Card mistake
                    elif add_all % 10 != 0:
                        print("Probably you made a mistake in the card number. Please try again!")

                    print("\n\n1. 33Balance\n"
                          "2. Add income\n"
                          "3. Do transfer\n"
                          "4. Close account\n"
                          "5. Log out\n"
                          "0. Exit")
                # Close account
                if acc_menu_select == 4:
                    cur.execute("DELETE FROM card WHERE number = :your_card",
                                {'your_card': your_card_number})
                    conn.commit()
                    print("The account has been closed!")
                    break

                # Log out
                if acc_menu_select == 5:
                    print("\nYou've successfully logged out\n")
                    print(
                        "1. Create an account\n"
                        "2. Log into account\n"
                        "0. Exit\n")
                    break
                # Exit
                elif acc_menu_select == 0:
                    print("Bye")
                    exit()
        # Wrong PIN
        else:
            print("Wrong card number or PIN!")
            print("\n\n1. Create an account\n"
                  "2. Log into account\n"
                  "0. Exit\n")
    # Exit
    elif menu_select == 0:
        print("Bye")
        exit()
