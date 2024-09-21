import random
import string
import pyperclip  # You'll need to install this package using: pip install pyperclip
import re

def generate_password(length=12, min_letters=1, min_numbers=1):
    if min_letters + min_numbers > length:
        raise ValueError("Minimum character requirements exceed password length.")

    while True:
        # Collect the required characters first
        password = []
        password += [random.choice(string.ascii_letters) for _ in range(min_letters)]
        password += [random.choice(string.digits) for _ in range(min_numbers)]

        # Fill the remaining length with random letters or numbers
        remaining_length = length - (min_letters + min_numbers)
        all_characters = string.ascii_letters + string.digits
        password += [random.choice(all_characters) for _ in range(remaining_length)]

        # Shuffle the password to randomize character positions
        random.shuffle(password)
        password_str = ''.join(password)

        # Ensure password meets conditions (regenerate if not)
        if (sum(c.isalpha() for c in password_str) >= min_letters and
            sum(c.isdigit() for c in password_str) >= min_numbers):
            return password_str

def check_password_strength(password):
    length = len(password)
    has_letters = any(char.isalpha() for char in password)
    has_numbers = any(char.isdigit() for char in password)

    # Check for patterns that weaken the password
    has_repeated_chars = bool(re.search(r'(.)\1\1', password))  # Three repeating chars
    is_sequential = password in string.ascii_lowercase or password in string.ascii_uppercase or password in string.digits

    if length >= 16 and has_letters and has_numbers and not (has_repeated_chars or is_sequential):
        return "Very Strong"
    elif length >= 12 and has_letters and has_numbers:
        return "Strong"
    elif length >= 8 and (has_letters or has_numbers):
        return "Medium"
    else:
        return "Weak"

def main():
    try:
        length = int(input("Enter the password length: "))

        if length <= 0:
            print("Password length must be greater than 0.")
            return

        min_letters = int(input("Minimum number of letters: "))
        min_numbers = int(input("Minimum number of numbers: "))

        if min_letters + min_numbers > length:
            print("Minimum number of characters exceeds total length.")
            return

        # Generate password
        password = generate_password(length, min_letters, min_numbers)

        # Ask user if they want to hide the password in the terminal
        hide_password = input("Do you want to hide the password? (y/n): ").strip().lower() == 'y'
        if hide_password:
            print("Password generated. (hidden for security)")
        else:
            print(f"Generated password: {password}")

        # Check password strength
        strength = check_password_strength(password)
        print(f"Password strength: {strength}")

        # Copy to clipboard
        pyperclip.copy(password)
        print("Password copied to clipboard.")
        
        # Ask to save the password to a file
        save_option = input("Do you want to save the password to a file? (y/n): ").strip().lower()
        if save_option == 'y':
            filename = input("Enter filename to save (default is 'password.txt'): ").strip() or "password.txt"
            with open(filename, "w") as file:
                file.write(password)
            print(f"Password saved to {filename}")

    except ValueError as e:
        print(f"Error: {e}. Please enter valid values.")

if __name__ == "__main__":
    main()
