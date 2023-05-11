Simple Banking System

This python code is a simple banking system simulation. It uses a SQLite database to store card numbers, their corresponding PINs, and account balances.

How It Works

Card Creation:
When a new card is created, the program generates a unique 16-digit card number, starting with "400000", followed by a 9-digit account identifier, and ending with a checksum digit. The checksum digit is calculated using the Luhn algorithm to ensure the card number's validity.

A 4-digit PIN is then randomly generated for the card.

Both the card number and PIN are stored in the 'card' table of the SQLite database.

Logging In:
Users can log into an account using their card number and PIN. If the provided credentials match those in the database, login is successful; otherwise, an error message is displayed.

Account Operations:
Once logged in, users can perform several operations:

Check Balance: Display the current account balance.
Add Income: Add income to the account balance.
Do Transfer: Transfer money to another account. The transfer is subjected to checks: Luhn algorithm validation, existence of the recipient's card in the database, and sufficient balance in the sender's account.
Close Account: Delete the account from the database.
Log Out: Log out from the account.
Exiting:
The program can be exited at any time by choosing the 'Exit' option.

Usage

To run the script, you need to have Python installed on your machine along with the sqlite3 and random modules. Then, you can simply run the script in a Python environment.

This script is a basic implementation of a banking system and is not intended for use in a real-world banking scenario. It is meant for educational and testing purposes only.

Future Improvements

In the future, additional features could be added, such as handling multiple currencies, managing multiple users, performing more complex transactions, etc. Contributions are welcome!
