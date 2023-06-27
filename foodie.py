import requests
import json
import random
import geocoder
import streamlit as st
import folium
from streamlit_folium import folium_static
import emoji


API_KEY = 'AIzaSyB0bYjUNU5jy8Uh7jbG5yzvvCG-1stFqLQ'

def get_public_ip_and_location():
    try:
        # Send HTTP GET request to a public IP API
        response = requests.get('https://api.ipify.org?format=json')

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()

            # Extract the public IP address from the response
            ip_address = data.get('ip')

            # Retrieve location information based on the IP address
            location_response = requests.get(f'https://ipapi.co/{ip_address}/json')
            if location_response.status_code == 200:
                location_data = location_response.json()

                # Extract the relevant location information
                city = location_data.get('city')
                region = location_data.get('region')
                country = location_data.get('country_name')
                longitude = location_data.get("longitude")
                latitude = location_data.get("latitude")

                info = [ip_address, latitude, longitude, city, region, country]
                # Return the public IP address and location information
                return info

    except requests.RequestException:
        pass

    # Return None if an error occurred or the data is not available
    return None, None, None, None

def get_restaurants(dietary_restrictions=None, budget=None, miles=None, location=""):
    # Retrieves approximate location using your IP Address
    info = get_public_ip_and_location()
    location = str(info[1]) + "," + str(info[2])
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
    exceptions = ["market", "store", "grocery", "butcher", "shoppe", "shop", "liquor", "spirits", "beer", "convenience"]
    for business in businesses: 
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
        coordinates = [business["coordinates"]["latitude"], business["coordinates"]["longitude"]]
        restaurants.append((name, rating, address, phone, categories, coordinates))

    # Filter the restaurants, Randomize the order of the restaurants, and return the top 3
    filtered_restaurants = [
        restaurant for restaurant in restaurants
        if not any(exception in categories for exception in exceptions)
    ]
    random.shuffle(filtered_restaurants)
    top_restaurants = filtered_restaurants[:3]

    return restaurants, top_restaurants

def print_info(restaurant):
    print(f" {restaurant[0]} - {restaurant[1]} stars")
    print(f"   {restaurant[2]}")
    print(f"   {restaurant[3]}")
    print(f"   Categories: {restaurant[4]}")
    print(f"   {restaurant[5]}")
    print()

def print_top(top_restaurants, miles):
    # Print the top 3 restaurants
    print(f"Here are the top 3 restaurants near you within a {miles} mile radius:")
    for i, restaurant in enumerate(top_restaurants):
        print(f"{i + 1}.")
        print_info(restaurant)


def randomize(restaurants, top_restaurants):
    pick = random.choice(restaurants)
    while(pick in top_restaurants):
        continue
    print_info(pick)

# Set up your Streamlit app
emoji_marker = emoji.emojize(":face_savoring_food:")
st.markdown(f"<h1 style='text-align: center;'>Welcome to Foodie{emoji_marker}</h1>",
            unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Your personalized food guide for nearby culinary delights!</h3>",
            unsafe_allow_html=True)

st.write("")  # Empty line
st.markdown("---")  # Separator line
st.write("") 

#Radius Distance
dist = st.slider("What is the maximum distance you're willing to travel? (in miles)", 1, 15, 1)

#Dietary Restrictions
dietary_restrictions = st.text_input("Enter any dietary restrictions (separated by commas, or leave blank): ")
dietary_restrictions = [r.strip() for r in dietary_restrictions.split(",")] if dietary_restrictions else None

#Get Price
budget_map = {
    'Cheap':1,
    'Moderate':2,
    'Expensive':3
}
selection = st.selectbox("Enter your budget: ", list(budget_map))
budget = budget_map[selection]

#Make map and center around user's location
info = get_public_ip_and_location()
m = folium.Map(location=[info[1], info[2]], zoom_start=11)

if st.button("Generate"):
    with st.spinner("Loading..."):
        folium.Marker(location=[info[1], info[2]], popup="You").add_to(m)
        restaurants, top_picks = get_restaurants(dietary_restrictions, budget, dist)
        if not top_picks:
            st.error("No restaurants found in the given area. Try new inputs!")
        for i, restaurant in enumerate(top_picks):
            st.info(f''' 
                    {i + 1}. {restaurant[0]} - {restaurant[1]} stars  
                    {restaurant[2]}  
                    {restaurant[3]}  
                    Categories: {restaurant[4]}
                    ''')
            folium.Marker(location=restaurant[5], popup=restaurant[0], icon=folium.Icon(icon=emoji_marker, color='red')).add_to(m)
        folium_static(m, width=700)

