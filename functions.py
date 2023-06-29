import requests
import json

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
    A dictionary containing the location's address, phone number, categories, and rating 
'''


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


coordinates = "41.7997986, -72.8259854"
name = "Dom's Coffee"
