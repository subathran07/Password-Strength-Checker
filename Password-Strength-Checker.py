import random
import string
import re
import math
import getpass

def calculate_entropy(password):
    character_set_size = 0
    if any(c.islower() for c in password):
        character_set_size += 26
    if any(c.isupper() for c in password):
        character_set_size += 26
    if any(c.isdigit() for c in password):
        character_set_size += 10
    if any(c in string.punctuation for c in password):
        character_set_size += len(string.punctuation)
    
    
    entropy = len(password) * math.log2(character_set_size) if character_set_size > 0 else 0
    return entropy

def check_password_strength(password):
    if len(password) < 8:
        return "\033[91m🔴 Too Short (Minimum 8 characters required)\033[0m", 0
    
    length_criteria = len(password) >= 8
    lower_criteria = any(c.islower() for c in password)
    upper_criteria = any(c.isupper() for c in password)
    digit_criteria = any(c.isdigit() for c in password)
    special_criteria = any(c in string.punctuation for c in password)
    
    score = sum([length_criteria, lower_criteria, upper_criteria, digit_criteria, special_criteria])
    entropy = calculate_entropy(password)
    
    strength = "\033[91m🔴 Weak\033[0m"
    if score == 5 and entropy > 60:
        strength = "\033[92m🟢 Very Strong\033[0m"
    elif score >= 4:
        strength = "\033[93m🟡 Strong\033[0m"
    elif score == 3:
        strength = "\033[94m🔵 Medium\033[0m"
    
    return strength, entropy

def generate_password(length=12):
    if length < 8:
        length = 8  # Ensure minimum password length
    
    all_chars = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = (
            random.choice(string.ascii_lowercase) +
            random.choice(string.ascii_uppercase) +
            random.choice(string.digits) +
            random.choice(string.punctuation) +
            ''.join(random.choices(all_chars, k=length-4))
        )
        password = ''.join(random.sample(password, len(password)))  # Shuffle to avoid patterns
        return password

def main():
    non_interactive = False
    try:
        while True:
            print("\n\033[96m🔐 === Password Strength Checker & Generator ===\033[0m")
            print("1️⃣  Check Password Strength")
            print("2️⃣  Generate Strong Password")
            print("3️⃣  Exit")
            try:
                choice = input("Enter your choice: ").strip()
            except (EOFError, OSError):
                non_interactive = True
                break
            
            if choice == '1':
                try:
                    password = getpass.getpass("🔑 Enter password to check: ").strip()
                    if not password:
                        print("\033[91m⚠️  Password cannot be empty!\033[0m")
                        continue
                    strength, entropy = check_password_strength(password)
                    print(f"Password Strength: {strength} (Entropy: {entropy:.2f} bits)")
                except (EOFError, OSError):
                    non_interactive = True
                    break
            
            elif choice == '2':
                length = input("📏 Enter desired password length (minimum 8): ").strip()
                if not length.isdigit() or int(length) < 8:
                    print("\033[91m⚠️  Invalid length! Using default length of 12.\033[0m")
                    length = 12
                else:
                    length = int(length)
                password = generate_password(length)
                print(f"🆕 Generated Password: \033[92m{password}\033[0m")
            
            elif choice == '3':
                print("👋 Exiting... \033[92mGoodbye!\033[0m")
                break
            
            else:
                print("\033[91m❌ Invalid choice! Please try again.\033[0m")
    except (EOFError, OSError):
        non_interactive = True
    
    if non_interactive:
        print("\n🤖 Running in non-interactive mode. Skipping user input.")
        test_passwords = ["password123", "StrongPass!23", "P@ssw0rd!", "12345678", "A1!b2@C3#"]
        for pwd in test_passwords:
            strength, entropy = check_password_strength(pwd)
            print(f"📝 Test Password: {pwd}, Strength: {strength}, Entropy: {entropy:.2f} bits")

if __name__ == "__main__":
    main()
