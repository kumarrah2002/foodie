import requests

# Define the API endpoint URL
url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
api_key = 'AIzaSyAhZzoiTUSBFlupc4G0fTROLZBJxaBH9F4'
# Set the parameters for the nearby search
parameters = {
    "location": "41.7997986,-72.8259854",  # Coordinates
    "radius": 5000,  # Search radius in meters
    # Type of place to search for (e.g., restaurant, cafe, etc.)
    "type": "restaurant",
    "key": api_key  # Replace with your own API key
}

# Send the GET request
response = requests.get(url, params=parameters)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Get the response data in JSON format
    data = response.json()

    # Process the response data
    if data["status"] == "OK":
        # Extract the list of places from the response
        places = data["results"]

        price_dict = {
            "Budget": 1,
            "Moderate": 2,
            "High-End": 3,
            "Luxury": 4
        }

        # Iterate over the places and access their details
        for place in places:
            name = place["name"]
            address = place["vicinity"]
            rating = place.get("rating", "N/A")
            location = place["geometry"]['location']
            price = place.get("price_level", "N/A")
            categories = place.get("types", [])
            try:
                open_or_closed = place['opening_hours']['open_now']
            except KeyError:
                open_or_closed = None  # Set a default value, such as False

            print(f"Name: {name}")
            print(f"Address: {address}")
            print(f"Rating: {rating}")
            print(f"Coordinates: {location}")
            for key, val in price_dict.items():
                if val == price:
                    print(f"Price: {key}")
            if price == 'N/A':
                print(f"Price: N/A")
            print(f"Categories: {categories}")
            if open_or_closed == True:
                print("Open")
            elif open_or_closed == False:
                print("Closed")
            print("-----")
        # print(places[3])
# print(json_data['candidates'][0]['geometry']['location'])
# print(json_data['candidates'][0]['name'])
# print(str(json_data['candidates'][0]['rating']) + " stars")
