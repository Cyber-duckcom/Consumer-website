#Code imports
import hashlib
import json
import os

#Bear logog
BEAR = "ʕ •ᴥ•ʔ"
#Date file Name
DATA_FILE = "FazBearUser.json"
#Reservation file
RESERVATION_FILE = "FazBearReservations.json"

#Load existing users
def load_users():
    return load_json(DATA_FILE, {})

#Loading exstisting reservations
def load_reservations():
    data = load_json(RESERVATION_FILE, [])
    return data if isinstance(data, list) else []

#Load json files
def load_json(filename, default):
    if not os.path.exists(filename):
        return default

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except (json.JSONDecodeError, OSError):
        print(f"Could not read {filename}. Starting with empty data.")
        return default

#save json files
def save_json(filename, data):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
        return True
    except OSError as error:
        print(f"Could not save {filename}: {error}")
        return False

#Saving users in the json file
def save_users(users):
    return save_json(DATA_FILE, users)

#password saving
def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

#User email formating
def is_valid_email(email):
    return "@" in email and "." in email.rsplit("@", 1)[-1]

#Where users register their acounts to login from 
def register(users):
    email = input("Please enter your email!: ").strip().lower()
    if not is_valid_email(email):
        print("Please enter a valid email address!")
        return False
    if email in users:
        print(
            "This user already has an account with Fazbear Entertainment. "
            f"Please try login! {BEAR}"
        )
        return False

    for _ in range(3):
        password = input("Enter Password: ").strip()
        if not password:
            print("Password cannot be empty!")
            continue
        if password != input("Confirm Password: ").strip():
            print("Passwords do not match!")
            continue

        users[email] = hash_password(password)
        if not save_users(users):
            users.pop(email, None)
            return False

        print(
            "Registration complete! Welcome to the Fazbear Family, where "
            f"fantasy and fun come to life! {BEAR}"
        )
        return True

    print("Too many invalid attempts!")
    return False

#Where user input their login information 
def login(users):
    email = input("Please type your email!: ").strip().lower()
    if email not in users:
        print(
            "Username not found. Enter your credentials again or "
            "register if you don't have an account!"
        )
        return False

    for _ in range(3):
        password = input("Enter Password: ").strip()
        if users[email] == hash_password(password):
            print(f"Welcome back! {BEAR}")
            return True
        print("Incorrect password!")

    print("Too many incorrect login attempts!")
    return False

#Saving the part reserves 
def save_reserve(reservation):
    reservations = load_reservations()
    reservations.append(reservation)
    return save_json(RESERVATION_FILE, reservations)

3#Were users go to save/make thier reservations
def reserve(users):
    email = input("Please enter the email for the booking: ").strip().lower()
    if email not in users:
        print("Please register or log in before making a booking!")
        return False
#Users input the date they wanna reserve
    date = input("Please enter the date you would like to reserve for: ").strip()
    if not date:
        print("Please enter a reservation date!")
        return False

    try:
        people = int(input("Please select the amount of people attending: ").strip())
    except ValueError:
        print("Please enter a whole number of people.")
        return False
    if people < 1 or people > 50:
        print("The party size must be between 1 and 50 people.")
        return False
#User info for booking such email/date/ and how many people are attending
    booking = {"email": email, "date": date, "people": people}
    if save_reserve(booking):
        print(f"Booking confirmed for {people} people on {date}! {BEAR}")
        return True
    return False

#The first thing that pop ups when users load up the program
def main(): #Start of Main
    print("Welcome to the Freddy Fazbear Pizza website!")
    users = load_users()

    while True:
        choice = input(
            "\nChoose an option: register, login, book, info, location, or exit: "
        ).lower().strip()

        if choice == "register":
            register(users)
        elif choice == "login":
            login(users)
        elif choice == "book":
            reserve(users)
        elif choice == "info":
            print(
                "Welcome to Freddy Fazbear's Pizza! We serve pizza, host "
                "birthday parties, and offer family-friendly entertainment."
            )
        elif choice == "location":
            print("Our location: 123 Fazbear Street, Hurricane, Utah.")
        elif choice == "exit":
            print(f"Goodbye! {BEAR}")
            break
        else:
            print("Please enter a valid option.")


if __name__ == "__main__":
    main()
#End of Main