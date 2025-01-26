import random
import string

def generate_password(min_length, numbers=True, special_characters=True):
    letters = string.ascii_letters
    digits = string.digits
    special = string.punctuation

    characters = letters
    if numbers:
        characters += digits
    if special_characters:
        characters += special

    pwd = ""
    meets_criteria = False
    has_number = False
    has_special = False
    has_uppercase = False
    has_lowercase = False

    while not meets_criteria or len(pwd) < min_length:
        new_char = random.choice(characters)
        pwd += new_char

        if new_char in digits:
            has_number = True
        if new_char in special:
            has_special = True
        if new_char.isupper():
            has_uppercase = True
        if new_char.islower():
            has_lowercase = True

        meets_criteria = True
        if numbers:
            meets_criteria = has_number
        if special_characters:
            meets_criteria = meets_criteria and has_special

    return pwd

def evaluate_password_strength(password):
    strength = 0
  
    if any(char.islower() for char in password):
        strength += 1
    if any(char.isupper() for char in password):
        strength += 1
    if any(char.isdigit() for char in password):
        strength += 1
    if any(char in string.punctuation for char in password):
        strength += 1

 
    if strength == 4:
        return "Strong"
    elif strength == 3:
        return "Medium"
    else:
        return "Weak"


min_length = int(input("Enter the minimum length of the password: "))
include_numbers = input("Include numbers? (y/n): ").strip().lower() == "y"
include_specials = input("Include special characters? (y/n): ").strip().lower() == "y"


password = generate_password(min_length, include_numbers, include_specials)


strength = evaluate_password_strength(password)


print("The generated password is:", password)
print("Password strength:", strength)
