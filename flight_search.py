import requests
import datetime as dt
from flight_data import FlightData

KIWI_ID = ""
KIWI_ENDPOINT_LOCATION = "https://api.tequila.kiwi.com/locations/query"
KIWI_ENDPOINT_SEARCH = "https://api.tequila.kiwi.com/v2/search"
KIWI_KEY = ""


class FlightSearch:

    def get_destination_code(self, city_name):

        header = {
            "apikey": KIWI_KEY
        }

        search_data = {
            "term": city_name,
            "location_types": "city",
        }
        print(city_name)
        response = requests.get(url=KIWI_ENDPOINT_LOCATION, headers=header, params=search_data)
        city_iata_code = response.json()["locations"][0]["code"]
        print(city_iata_code)

        return city_iata_code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        headers = {"apikey": KIWI_KEY}
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 5,
            "nights_in_dst_to": 30,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "EUR",
        }

        response = requests.get(
            url=f"{KIWI_ENDPOINT_SEARCH}",
            headers=headers,
            params=query,
        )

        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No direct flights were found for {destination_city_code}. Looking for flights with one stopover.")

            # try flights with one stop over
            query["max_stopovers"] = 2

            response = requests.get(
                url=f"{KIWI_ENDPOINT_SEARCH}",
                headers=headers,
                params=query,
            )
            try:
                data = response.json()["data"][0]
            except IndexError:
                print(f"also no flight with maximum of 2 stopovers in total found for {destination_city_code}.")
                return None
            else:
                # Case 2 proceeding
                flight_data = FlightData(
                    price=data["price"],
                    origin_city=data["route"][0]["cityFrom"],
                    origin_airport=data["route"][0]["flyFrom"],
                    destination_city=data["route"][1]["cityTo"],
                    destination_airport=data["route"][1]["flyTo"],
                    out_date=data["route"][0]["local_departure"].split("T")[0],
                    return_date=data["route"][2]["local_departure"].split("T")[0],
                    airline=data["airlines"][0],
                    nr_stop_overs=len(data["route"])/2,
                    via_city=data["route"][0]["cityTo"]
                )
                print(f"found a flight via {flight_data.via_city}: €{flight_data.price} with {flight_data.airline}")
                return flight_data

        # Case 1 proceeding
        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0],
                airline=data["airlines"][0],
            )
            print(f"{flight_data.destination_city}: €{flight_data.price} with {flight_data.airline}")
            return flight_data

