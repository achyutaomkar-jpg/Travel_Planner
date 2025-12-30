import json

def load_places(): # This function loads the json file which contains the location data
    with open("places.json", "r") as f:
        return json.load(f)  


def filter_locations(city, category): # This function filters the locations based on city and category
    places = load_places()
    return [
        place for place in places
        if place['city'].strip().lower() == city.strip().lower()
        and place['type'].strip().lower() == category.strip().lower()
    ]




def rank_places(places): # This function will rank the location based on higher rating
    if not places:
        return []

    return sorted(places, key=lambda x: x['rating'], reverse=True)


    
def max_places(places, max_days): # This function is to return the maximum number of places to visit in a day
    return places[:max_days]




def select_info(places): # This will return the required information like place name, category and rating
    return [
        {
            "name": place["name"],
            "category": place["type"],
            "rating": place["rating"]
        }
        for place in places
    ]



def group_places_by_day(places, days): # This function creates an itenary which will list the locations to visit per day
    itinerary = {f"Day {i+1}": [] for i in range(days)} # This creates an empty itenary list to store the locations
    
    for idx, place in enumerate(places): # This will loop through the places dictionary (idx=index, place=actual place dictionary)
        day = f"Day {(idx % days) + 1}" # This will equally seperate the places for each day
        itinerary[day].append(place) # This will add the place to the correct day
    
    return itinerary




from langchain.tools import tool
@tool # we will wrap this tool just like other tools

def location_search_tool(city: str, category: str, max_days: int):
    """
    This shows the maximum number of locations could be visited based on the city and category
    """
    places = filter_locations(city, category)
    best_locations = rank_places(places)
    limited = max_places(best_locations, max_days)
    result = select_info(limited)
    day_wise_itinerary = group_places_by_day(result, max_days)

    return {
       "itinerary": day_wise_itinerary
    }


# Here we can test the logic of the tool
output = location_search_tool.run({
    "city": "Goa",
    "category": "market",
    "max_days": 3,
})

print(output)