import requests
import json
import random
import geocoder
import googlemaps

API_KEY = 'AIzaSyB0bYjUNU5jy8Uh7jbG5yzvvCG-1stFqLQ'


def get_restaurants(dietary_restrictions=None, budget=None, miles=None):
    # Retrieves approximate location using your IP Address
    g = geocoder.ipinfo('me')
    location = str(g.lat) + "," + str(g.lng)
    # Convert radius from miles to meters
    if miles is not None and isinstance(miles, int) and int(miles) <= 15:
        radius = int(miles * 1609.34)  # Convert miles to meters
    else:
        radius = None

    # Yelp API endpoint and parameters
    yelp_endpoint = "https://api.yelp.com/v3/businesses/search"
    yelp_headers = dict(
        Authorization="Bearer 8V0wD0XaZNVI7vNZ4wBoDyWs_CR7jUemUzrGjlYfB6vnquwXf2fvTKH9-lW-s9F6viimgNrbF8hR-VQlt-f3ZL1cIRvkXfDKftN04GxUOv40TDqjFjiouQOnkjo8ZHYx"
    )
    yelp_parameters = {
        "location": location,
        "categories": "food,restaurants",
        "limit": 50  # limit to the top 50 results
    }

    # Add dietary restrictions, budget, and radius to the parameters
    if dietary_restrictions:
        yelp_parameters["attributes"] = ",".join(dietary_restrictions)

    if budget:
        yelp_parameters["price"] = budget

    if radius:
        yelp_parameters["radius"] = radius

    # Make the Yelp API request and parse the response
    yelp_response = requests.get(yelp_endpoint, headers=yelp_headers, params=yelp_parameters)
    yelp_data = json.loads(yelp_response.text)
    # Extract the relevant data from the Yelp response
    businesses = yelp_data["businesses"]
    restaurants = []
    exceptions = ["market", "store", "grocery", "butcher", "shoppe", "shop", "liquor", "spirits", "beer"]
    for business in businesses:  # rewrite exceptions
        for keyword in exceptions:
            for item in business["categories"]:
                if keyword in item['alias'].lower():
                    continue  # ignore businesses with exception keywords (like "market" or "store") in their name
        name = business["name"]
        rating = business["rating"]
        distance = business["distance"]
        # print(business["coordinates"]) ["latitude"] or ["longitude"]
        if (distance > radius):
            continue
        if (rating < 4):
            continue  # ignore businesses with ratings less than 4 or greater than radius inputted
        address = ", ".join(business["location"]["display_address"])
        phone = business["phone"]
        categories = ",".join([cat["title"] for cat in business["categories"]])
        restaurants.append((name, rating, address, phone, categories))

    # Randomize the order of the restaurants and return the top 3
    random.shuffle(restaurants)
    top_restaurants = restaurants[:3]

    return restaurants, top_restaurants

def print_info(top_restaurants, miles):
    # Print the top 3 restaurants
    print(f"Here are the top 3 restaurants near you within a {miles} mile radius:")
    for i, restaurant in enumerate(top_restaurants):
        print(f"{i + 1}. {restaurant[0]} - {restaurant[1]} stars")
        print(f"   {restaurant[2]}")
        print(f"   {restaurant[3]}")
        print(f"   Categories: {restaurant[4]}")
        print()


def randomize(restaurants):
    pick = random.choice(restaurants)
    print(f"{pick[0]} - {pick[1]} stars")
    print(f"   {pick[2]}")
    print(f"   {pick[3]}")
    print(f"   Categories: {pick[4]}")
    print()

while True:
    dist = input("What is your search radius (in miles)? ")
    dist = int(dist)
    if (dist > 15 or dist < 0):
        dist = input("Please input a radius distance of up to 15 miles: ")
        dist = int(dist)
    elif (dist is None):
        dist = input("Enter a radius distance of up to 15 miles: ")
        dist = int(dist)
    # Prompt the user to enter any dietary restrictions
    dietary_restrictions = input("Enter any dietary restrictions (separated by commas, or leave blank): ")
    dietary_restrictions = [r.strip() for r in dietary_restrictions.split(",")] if dietary_restrictions else None

    # Prompt the user to enter a budget
    budget = input("Enter your budget (1 for cheap, 2 for moderate, 3 for expensive, or leave blank): ")
    budget = budget if budget in ["1", "2", "3"] else None

    # Call the get_restaurants function with the user's inputs
    restaurants, top_picks = get_restaurants(dietary_restrictions, budget, dist)
    print_info(top_picks, dist)

    rand = input("Would You Like An Option Picked For You? (Y/n) ")
    if rand == 'Y':
        randomize(restaurants)
    cont = input("Would You Like To Continue? (Y/n) ")
    if cont != 'Y':
        break

