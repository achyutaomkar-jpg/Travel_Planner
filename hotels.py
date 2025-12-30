import json

def load_hotels(): # Here we create a function which loads the required json file
    with open("hotels.json", "r") as f:
        return json.load(f)  


def filter_hotels(city, rating, price): # This function will filter the hotels based on city, rating and price per night
    hotels = load_hotels() # This will load the json file with the hotel data
    return [
        hotel for hotel in hotels
        if hotel["city"].lower() == city.lower()
        and int(hotel["stars"]) >= rating
        and int(hotel["price_per_night"]) <= price  # This will return the hotels with given city, higher rating and lower price per night
    ]


def rank_hotels(hotels, preference='cheapest'): # This function will rank the hotels based on high rating and low price
    if not hotels:
        return None
    if preference == "highest_rating": # this if block will be executed if user preference is higher rating
        return max(hotels, key=lambda x: x['stars']) # this will return the hotel with maximun rating

    return min(hotels, key=lambda x: x['price_per_night']) # if user preference is cheaper price, this will return cheaper hotels



from langchain.tools import tool
@tool # then we will wrap the tool in langchain framework just like we did with the flight search tool
def hotel_search_tool(city: str, price: int, rating: int, preference: str):
    """
    Finds the Best Hotels based on city with Highest Rating or Lowest Price_Per_Night
    """
    hotels = filter_hotels(city, rating, price)
    best_hotels = rank_hotels(hotels, preference)
    

    if not best_hotels:
        result = {
            "message": f"No hotels found in {city} within price ${price} and rating {rating}+."
        }
        return result

    return {
        "hotel": {
            "name": best_hotels['name'],
            "price": best_hotels["price_per_night"],
            "rating": best_hotels['stars'],
            "amenities": best_hotels['amenities']  
        },
        "message": f"Best hotel in {city}: {best_hotels['name']} at ${best_hotels['price_per_night']} per night."
    }


# Now we can test the tool
output = hotel_search_tool.run({
    "city": "Delhi",
    "price": 4783,
    "rating": 2,
    "preference": "cheapest"
})

print(output)