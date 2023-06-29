from functions import nearby_search, text_search, print_results

miles = 10
meters = miles * 1609.34
location = "41.7997986, -72.8259854"

if __name__ == '__main__':
    # locations = nearby_search(location, meters)
    # print_results(locations, 3)

    search_locations = text_search("thai", location, meters)
    for loc in search_locations:
        print(loc["name"] + ': ' + loc["formatted_address"])


