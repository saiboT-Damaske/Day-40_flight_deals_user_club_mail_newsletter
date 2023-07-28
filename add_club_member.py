import sheety

SHEETY_USERS = ""

first_name = input("Enter your first name: ").title()
last_name = input("Enter your last name: ").title()
email_1 = input("Email: ")
email_2 = input("Confirm email: ")

while email_1 != email_2:
    email_1 = input("What is your email? ")
    if email_1.lower() == "quit" \
            or email_1.lower() == "exit":
        exit()
    email_2 = input("Please verify your email : ")
    if email_2.lower() == "quit" \
            or email_2.lower() == "exit":
        exit()


print("You are in the club!")

sheety.add_new_user(first_name, last_name, email_1)


