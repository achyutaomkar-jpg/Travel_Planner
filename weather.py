
import requests

def get_city_coordinates(city): # This function uses the open metep api, to return the city coordinates (latitude and longitude)
    url = "https://geocoding-api.open-meteo.com/v1/search" # This is the url for the api
    params = {
        "name": city,
        "count": 1 # Count = 1 will only return the one best match
    }

    response = requests.get(url, params=params) # we sent the response to the API and store the data in a json file
    data = response.json()

    if "results" not in data:
        return None

    location = data["results"][0]
    return location["latitude"], location["longitude"] # here we will return the city coordinates



def fetch_weather(lat, lon, start_date, end_date): # The next step is to fetch the weather report
    url = "https://api.open-meteo.com/v1/forecast" # this url is for the API, which provides weather forecast
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "daily": ["temperature_2m_max", "temperature_2m_min", "weathercode"],
        "timezone": "auto"
    }

    response = requests.get(url, params=params)
    data = response.json()

    return data  # this will returm the data for the particular coordiantes between the given start and end dates 


# The next to step is to create a text file which contains weather code with their respective description
def load_weather_codes(file_path): # this function is used to load the text file with the weather codes
    codes = {}
    with open(file_path, "r") as f: # here we open the file
        for line in f: # we loop through every line 
            line = line.strip() # we will remove the empty spaces
            if line:  # we will skip empty lines
                try:
                    code, desc = line.split("=") # then we will split the line based on '=', left of '=' is code and right is text
                    codes[int(code.strip())] = desc.strip()  # convert code to int
                except ValueError:
                    print(f"Skipping invalid line: {line}")
    return codes

# this will store the codes in the variable WEATHER_CODES
WEATHER_CODES = load_weather_codes("weather.txt")

def format_weather(data): # This function will return the weather forecast data
    daily_forecast = []
    times = data["daily"]["time"]
    max_temps = data["daily"]["temperature_2m_max"]
    min_temps = data["daily"]["temperature_2m_min"]
    weathercodes = data["daily"]["weathercode"]

    for i in range(len(times)):
        daily_forecast.append({
            "date": times[i],
            "condition": WEATHER_CODES.get(weathercodes[i], "Unknown"), # here we will get the weather codes from the text file
            "temp_range": f"{min_temps[i]}–{max_temps[i]} °C" # here we will return the temperature range
        })

    return daily_forecast



from langchain.tools import tool
@tool # This is the lang chain framework to wrap the tool
def weather_lookup_tool(city: str, start_date: str, end_date: str):
    """
    Provides daily weather forecast for a city between given dates.
    """

    
    coords = get_city_coordinates(city)
    if not coords:
        return {"message": "City not found"}

    lat, lon = coords
    raw_data = fetch_weather(lat, lon, start_date, end_date)
    formatted = format_weather(raw_data)

    return formatted


# This is to test the tool
result = weather_lookup_tool.run({
    "city": "Delhi",
    "start_date": "2025-12-17",
    "end_date": "2025-12-19"
})

print(result)