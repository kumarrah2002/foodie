import requests
import json
import random

# Access Google Maps Places API
nearbysearch_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
textsearch_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

api_key = 'AIzaSyAhZzoiTUSBFlupc4G0fTROLZBJxaBH9F4'

# Access Yelp API
yelp_endpoint = "https://api.yelp.com/v3/businesses/search"
yelp_headers = dict(
    Authorization="Bearer 8V0wD0XaZNVI7vNZ4wBoDyWs_CR7jUemUzrGjlYfB6vnquwXf2fvTKH9-lW-s9F6viimgNrbF8hR-VQlt-f3ZL1cIRvkXfDKftN04GxUOv40TDqjFjiouQOnkjo8ZHYx"
)

'''
Purpose: Looks Up Yelp Location Using Yelp Api
Parameters:
    name: Location Name
    location: Coordinates (string format)
Return: 
    A dictionary 
    containing the location's address, phone number, categories, and rating 
'''


# def exceptions():

def join_yelp(name, location):
    params = {
        'location': location,
        "categories": "food,restaurants",
        'term': name,
        'limit': 1
    }

    response = requests.get(yelp_endpoint, headers=yelp_headers, params=params)
    if response.status_code == 200:
        data = json.loads(response.text)
        if "businesses" in data and len(data["businesses"]) > 0:
            business = data["businesses"][0]
            address = ", ".join(business["location"]["display_address"])
            categories = ",".join([cat["title"]
                                   for cat in business["categories"]])
            phone = business["phone"]
            rating = business["rating"]
            return {
                "address": address,
                "phone": phone,
                "yelp_categories": categories,
                "yelp_rating": rating}


def print_results(places, num_locations):
    price_dict = {
        "Budget": 1,
        "Moderate": 2,
        "High-End": 3,
        "Luxury": 4
    }

    random.shuffle(places)
    # Iterate over the places and access their details
    for i, place in enumerate(places[:num_locations]):  # [:5]
        name = place["name"]
        address = place['vicinity']
        google_rating = place.get("rating", "N/A")
        location = place["geometry"]['location']
        location = f"{location['lat']}, {location['lng']}"
        price = place.get("price_level", "N/A")
        categories = place.get("types", [])
        try:
            open_or_closed = place['opening_hours']['open_now']
        except KeyError:
            open_or_closed = None  # Set a default value

        # Function contains a list of the location address,
        restaurant = join_yelp(name, location)

        print(f"{i + 1} - Name: {name}")
        if restaurant is not None and google_rating != 'N/A':
            print(f"Address: {restaurant['address']}")
            rating = round(
                (float(google_rating) + float(restaurant["yelp_rating"])) / 2, 1)
            print(f"Rating: {rating}")
            print(f"Categories: {categories}")
            print(f"Yelp Categories: {restaurant['yelp_categories']}")
        else:
            print(f"Address: {address}")
            print(f"Rating: {google_rating}")
            print(f"Categories: {categories}")

        print(f"Coordinates: {location}")

        for key, val in price_dict.items():
            if val == price:
                print(f"Price: {key}")
        if price == 'N/A':
            print(f"Price: N/A")

        if open_or_closed:
            print("Open")
        elif not open_or_closed:
            print("Closed")
        print("-----")


def nearby_search(location, meters):
    googlemaps_parameters = {
        "location": location,  # Coordinates
        "radius": meters,  # Search radius in meters
        # Type of place to search for (e.g., restaurant, cafe, etc.)
        "type": "restaurant",
        "key": api_key  # Replace with your own API key
    }

    google_response = requests.get(nearbysearch_url, params=googlemaps_parameters)

    # Check if the request was successful (status code 200)
    if google_response.status_code == 200:
        # Get the response data in JSON format
        data = google_response.json()

        # Process the response data
        if data["status"] == "OK":
            # Extract the list of places from the response
            places = data["results"]
            return places


        else:
            print("Unable to process request.")

    else:
        print("Unable to process request")


def text_search(text, location, meters):
    googlemaps_parameters = {
        "query": text,
        "radius": meters,  # Search radius in meters
        "location": location,  # Coordinates
        # Type of place to search for (e.g., restaurant, cafe, etc.)
        "key": api_key  # Replace with your own API key
    }

    google_response = requests.get(textsearch_url, params=googlemaps_parameters)

    # Check if the request was successful (status code 200)
    if google_response.status_code == 200:
        # Get the response data in JSON format
        data = google_response.json()

        # Process the response data
        if data["status"] == "OK":
            # Extract the list of places from the response
            places = data["results"]
            return places


        else:
            print("Unable to process request.")

    else:
        print("Unable to process request")
