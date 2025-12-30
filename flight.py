import json

def load_flights(): # Here we create a function which loads the required json file
    with open("flights.json", "r") as f:
        return json.load(f)  



# Now we filter flights based on source and destination
def filter_flights(source, destination): # here we create a function which filters the flights
    flights = load_flights() # here we call the load fucntion, because we need the json file which contains the flight data
    return [
        flight for flight in flights
        if flight["from"].strip().lower() == source.strip().lower()
        and flight["to"].strip().lower() == destination.strip().lower() # Now we return the flights source and destination
    ]




# Now we will create a function to rank flights from Cheapest or Fastest

# Before the function, first we have to calculate the duration based on departure time and arrival time

from datetime import datetime

def calculate_duration(departure_time, arrival_time):
    departure = datetime.fromisoformat(departure_time) # it converts the date time string into date time python object
    arrival = datetime.fromisoformat(arrival_time)
    duration = arrival - departure # here we will calculate the duration
    return duration.total_seconds() / 60  # we will convert the duration into minutes




def select_best_flight(flights, preference='cheapest'): # This function selects best flight based on user preference (cheapest or fastest)
    if not flights: # This if block returns "None", if the list of flights is empty instead of runtime error
        return None

    if preference == "fastest": # If user preference is fastest flight, then this if block will be executed
        return min(
            flights,
            key=lambda x: calculate_duration(
                x["departure_time"], x["arrival_time"] # here we call the function to calculate the duration
            )
        ) # this will return the flight with minimum duration

    return min(flights, key=lambda x: x["price"]) # if user preference is cheapest, this will return cheaper flight




# Now we will create a lang-chain framework, used to help the AI think step by step, and use tools we created to perform real tasks.
from langchain.tools import tool

@tool # this decorator wraps the function into an object called tool, which the agent can use.
# it also adds extra behaviour like: argument handling, structured output.
def flight_search_tool(source: str, destination: str, preference: str): 
    """
    Finds the best flight given a source, destination, and user preference (cheapest or fastest).
    """ # This doctstring tells the agent what the tool does.
    flights = filter_flights(source, destination) # this calls the funstion to filter the flight based on source and destination
    best = select_best_flight(flights, preference) # this calls the function to select the best flight based on user preference
    if not best:
        result = {
            "message": f"No flights found from {source} to {destination}."
        }
        return result
        
    duration = calculate_duration(best["departure_time"], best["arrival_time"])
    result = {
        "flight": {
            "airline": best["airline"],
            "price": best["price"],
            "duration_minutes": duration,
            "departure_time": best["departure_time"]
        },
        "message": f"Best flight from {source} to {destination}: {best['airline']} at ${best['price']}."
    } # this will the return the best flight information like airline, price, duration in minutes and departure time

    return result


# This gives the structured output
output = flight_search_tool.invoke({
    "source": "Hyderabad",
    "destination": "Delhi",
    "preference": "fastest"
})

print(output)