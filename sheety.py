import requests

SHEETY_USERS = ""


def add_new_user(first_name, last_name, email):
    user_data = {
        "user": {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
        }
    }
    response = requests.post(url=SHEETY_USERS, json=user_data)
    response.raise_for_status()
    print(response.text)


def get_users():
    response = requests.get(url=SHEETY_USERS)
    response.raise_for_status()
    data = response.json()["users"]
    return data



