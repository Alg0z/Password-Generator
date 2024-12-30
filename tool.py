import hashlib
import random
import string
import requests
import zxcvbn

def check_password(password):
    sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)
    if response.status_code == 200:
        for line in response.text.splitlines():
            p, count = line.split(":")
            if p == suffix:
                return True, count
            return False, 0
def generate_password(length=16, use_upper=True, use_lower=True, use_numbers=True, use_special=True):
    if length < 6:
        raise ValueError("Password length must be at least 6")
    pool = ""
    if use_upper: pool += string.ascii_uppercase
    if use_lower: pool += string.ascii_lowercase
    if use_numbers: pool += string.digits
    if use_special: pool += "!@#$%^&*(),.?\":{}|<>"
    if not pool:
        raise ValueError("No char types selected")
    return ''.join(random.choice(pool) for _ in range(length))
def evaluate_strength(password):
    is_pwned, count = check_password(password)
    if is_pwned:
        print(f"Weak: This password has been found in {count} breaches!!")
    else:
        print("Password is not in any breaches :)")
    strength = zxcvbn.zxcvbn(password)
    score = strength['score']
    feedback = strength['feedback']
    if score == 0:
        print("Very Weak: " + feedback.get('suggestions', ['Consider a much stronger password :)'])[0])
    elif score == 1:
        print("Weak: " + feedback.get('suggestions', ['Consider a much stronger password :)'])[0])
    elif score == 2:
        print("Moderate: " + feedback.get('suggestions', ['Pretty cool i guess :P'])[0])
    elif score == 3:
        print("Strong: " + feedback.get('suggestions', ['Awesome password!'])[0])
    else:
        print("Woosh! That's a tough password...")
def main():
    print("// Password Evaluator and Generator")
    while True:
        print("\n1> Generate Password")
        print("2> Evaluate Password Strength")
        print("3> Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            length = int(input("Enter password length (min 6): ").strip())
            use_upper = input("Include uppercase? y/n ").strip().lower() == "y"
            use_lower = input("Include lowercase? y/n ").strip().lower() == "y"
            use_numbers = input("Include numbers? y/n ").strip().lower() == "y"
            use_special = input("Include special characters? y/n ").strip().lower() == "y"
            try:
                password = generate_password(length, use_upper, use_lower, use_numbers, use_special)
                print(f"\nGenerated Password: {password}")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == "2":
            password = input("Enter password to ev: ").strip()
            evaluate_strength(password)
        elif choice == "3":
            print("Exiting...")
        else:
            print("Invalid.")

if __name__ == "__main__":
    main()
            # WTF LOL I FORGOT THE PWNED
            # NICE :P