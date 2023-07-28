# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager
# classes to achieve the program requirements.

from pprint import pprint

import datetime as dt

import sheety
from data_manager import DataManager
from notification_manager import NotificationManager
from flight_search import FlightSearch

FLY_FROM_IATA = "MUC"

data_manager = DataManager()
notification_manager = NotificationManager()
sheet_data = data_manager.get_destination_data()
flight_searcher = FlightSearch()


# --------------- get iaTa codes for city names ------------------ #


if sheet_data[0]["iataCode"] == "":
    from flight_search import FlightSearch

    flight_search = FlightSearch()
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    print(f"sheet_data:\n {sheet_data}")

    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()



# --------------- get cheapest prices ------------------ #

# call flight search method and check for prices
tomorrow = dt.datetime.now() + dt.timedelta(days=1)
six_month_from_today = dt.datetime.now() + dt.timedelta(days=(6 * 30))

for destination in sheet_data:
    # for each row of destinations, search for the cheapest available flight in a timeframe from tomorrow to in 6 months
    flight = flight_searcher.check_flights(
        FLY_FROM_IATA,
        destination["iataCode"],    # each city as destination
        from_time=tomorrow,
        to_time=six_month_from_today
    )
    if flight is not None:
        print(f"old low: {destination['lowestPrice']}€ vs this price: {flight.price}€")


        # ---------------- check if any prices were cheaper ----------------- #
        if destination['lowestPrice'] > flight.price:
            new_lowest_price = flight.price

        # ----------------- send message alert --------------------- #
            if flight.stop_overs > 0:
                message += f"Subject: New price alert 👂✈️🌍\n" \
                           f"Dear {user['firstName']}, \n" \
                           f"Only {new_lowest_price}€ to fly from " \
                           f"{flight.origin_city}-{flight.origin_airport} to " \
                           f"{flight.destination_city}-{flight.destination_airport} via " \
                           f"{flight.via_city}, from " \
                           f"{flight.out_date} to {flight.return_date}"
            else:
                message = f"New price alert 👂✈️🌍\n" \
                      f"Only {new_lowest_price}€ to fly from " \
                      f"{flight.origin_city}-{flight.origin_airport} to " \
                      f"{flight.destination_city}-{flight.destination_airport}, from " \
                      f"{flight.out_date} to {flight.return_date}"

            notification_manager.send_low_price_alert(message=message)

        # ---------------- send email alert to flight club ------------ #
            user_data = sheety.get_users()
            for user in user_data:
                if flight.stop_overs > 0:
                    message += f"Subject: New price alert 👂✈️🌍\n" \
                          f"Dear {user['firstName']}, \n" \
                          f"Only {new_lowest_price}€ to fly from " \
                          f"{flight.origin_city}-{flight.origin_airport} to " \
                          f"{flight.destination_city}-{flight.destination_airport} via " \
                               f"{flight.via_city}, from " \
                          f"{flight.out_date} to {flight.return_date}"
                else:
                    message = f"Subject: New price alert 👂✈️🌍\n" \
                          f"Dear {user['firstName']}, \n" \
                          f"Only {new_lowest_price}€ to fly from " \
                          f"{flight.origin_city}-{flight.origin_airport} to " \
                          f"{flight.destination_city}-{flight.destination_airport}, from " \
                          f"{flight.out_date} to {flight.return_date}"
                message = message.encode("utf-8").strip()
                notification_manager.send_club_member_deals(to_email=user["email"], message=message)
