# ----------------------------------
# Import Streamlit for building the UI
# ----------------------------------
import streamlit as st

# ----------------------------------
# Import date utilities to handle travel dates
# ----------------------------------
from datetime import date, timedelta

# ----------------------------------
# Import all tools and data loaders
# These come from the modular tool files
# ----------------------------------
from flight import load_flights, flight_search_tool
from hotels import load_hotels, hotel_search_tool
from places import load_places
from weather import weather_lookup_tool
from budget import budget_estimation_tool

# ----------------------------------
# Streamlit Page Configuration
# Sets browser tab title and icon
# ----------------------------------
st.set_page_config(page_title="Flight Planner", page_icon="✈️")

# Main title shown on the page
st.title("✈️ Flight Planner")

# ----------------------------------
# Load all static data from JSON files
# This avoids reloading files repeatedly
# ----------------------------------
flights = load_flights()
hotels = load_hotels()
places = load_places()

# ----------------------------------
# Extract unique source and destination cities
# Used to populate dropdowns
# ----------------------------------
sources = sorted(set(f["from"] for f in flights))
destinations = sorted(set(f["to"] for f in flights))

# ----------------------------------
# Initialize Streamlit Session State
# Session state stores data across user interactions
# ----------------------------------
defaults = {
    "flight_result": None,
    "hotel_result": None,
    "weather_result": None,
    "budget_result": None,
    "final_destination": None,
    "recommended": [],
    "recommended_prices": [],
    "show_recommendation": False,
    "show_hotel_recommendation": False,
    "days": 3
}

# Populate session state with default values if missing
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ----------------------------------
# Helper Function:
# Suggest alternative destinations if no direct flights exist
# ----------------------------------
def recommend_destinations(flights, source):
    return sorted(set(
        f["to"] for f in flights
        if f["from"].lower() == source.lower()
    ))

# ----------------------------------
# Helper Function:
# Suggest hotel prices if chosen budget has no hotels
# ----------------------------------
def recommend_hotel_prices(hotels, city):
    return sorted(set(
        int(h["price_per_night"])
        for h in hotels
        if h["city"].lower() == city.lower()
    ))

# ----------------------------------
# FLIGHT INPUT SECTION
# User selects source, destination, and preference
# ----------------------------------
source = st.selectbox("Source City", sources)
destination = st.selectbox("Destination City", destinations)
preference = st.radio("Preference", ["fastest", "cheapest"])

# ----------------------------------
# FLIGHT SEARCH BUTTON
# Calls flight search tool when clicked
# ----------------------------------
if st.button("Search Flight"):
    result = flight_search_tool.run({
        "source": source,
        "destination": destination,
        "preference": preference
    })

    # If flight is found, store result in session
    if "flight" in result:
        st.session_state.flight_result = result
        st.session_state.final_destination = destination
        st.session_state.show_recommendation = False
    else:
        # If no flight found, recommend other destinations
        st.session_state.flight_result = None
        st.session_state.recommended = recommend_destinations(flights, source)
        st.session_state.show_recommendation = True

# ----------------------------------
# FLIGHT RECOMMENDATION SECTION
# Shown only when no direct flights exist
# ----------------------------------
if st.session_state.show_recommendation:
    st.warning("No direct flights. Try these destinations:")

    rec_city = st.selectbox(
        "Recommended Destination",
        st.session_state.recommended
    )

    if st.button("Search Recommended Flight"):
        result = flight_search_tool.run({
            "source": source,
            "destination": rec_city,
            "preference": preference
        })

        st.session_state.flight_result = result
        st.session_state.final_destination = rec_city
        st.session_state.show_recommendation = False

# ----------------------------------
# FLIGHT OUTPUT SECTION
# Displays selected flight details
# ----------------------------------
if st.session_state.flight_result:
    st.divider()
    st.subheader("✈️ Flight Selected")
    st.json(st.session_state.flight_result)

# ----------------------------------
# HOTEL SEARCH SECTION
# Activated only after flight selection
# ----------------------------------
if st.session_state.flight_result:

    st.divider()
    st.subheader("🏨 Hotel Search")

    # User selects maximum hotel price
    max_price = st.slider(
        "Max price per night",
        1000, 8000, 3000, 500
    )

    if st.button("Search Hotels"):
        hotel = hotel_search_tool.run({
            "city": st.session_state.final_destination,
            "price": max_price,
            "rating": 1,
            "preference": "cheapest"
        })

        # If hotel found, save it
        if "hotel" in hotel:
            st.session_state.hotel_result = hotel
            st.session_state.show_hotel_recommendation = False
        else:
            # Else recommend price ranges
            st.session_state.hotel_result = None
            st.session_state.recommended_prices = recommend_hotel_prices(
                hotels,
                st.session_state.final_destination
            )
            st.session_state.show_hotel_recommendation = True

# ----------------------------------
# HOTEL PRICE RECOMMENDATION
# ----------------------------------
if st.session_state.show_hotel_recommendation:
    st.warning("No hotels in this price range. Try these prices:")

    price = st.selectbox(
        "Recommended Hotel Price",
        st.session_state.recommended_prices
    )

    if st.button("Search Hotel with Recommended Price"):
        hotel = hotel_search_tool.run({
            "city": st.session_state.final_destination,
            "price": price,
            "rating": 1,
            "preference": "cheapest"
        })

        st.session_state.hotel_result = hotel
        st.session_state.show_hotel_recommendation = False

# ----------------------------------
# HOTEL OUTPUT SECTION
# ----------------------------------
if st.session_state.hotel_result:
    st.subheader("🏨 Hotel Selected")
    st.json(st.session_state.hotel_result)

# ----------------------------------
# PLACES + WEATHER SECTION
# ----------------------------------
if st.session_state.final_destination:

    st.divider()
    city = st.session_state.final_destination
    st.subheader(f"📍 Exploring {city}")

    # User selects number of travel days
    days = st.number_input(
        "Number of days",
        1, 10, st.session_state.days
    )
    st.session_state.days = days

    # Calculate start and end dates
    start = date.today()
    end = start + timedelta(days=days - 1)

    # Fetch weather data
    weather = weather_lookup_tool.run({
        "city": city,
        "start_date": start.isoformat(),
        "end_date": end.isoformat()
    })

    st.session_state.weather_result = weather

# ----------------------------------
# WEATHER OUTPUT SECTION
# ----------------------------------
if st.session_state.weather_result:
    st.subheader("🌤️ Weather Forecast")

    for d in st.session_state.weather_result:
        st.markdown(
            f"**{d['date']}** – {d['condition']} ({d['temp_range']})"
        )

# ----------------------------------
# PLACES / ITINERARY SECTION
# ----------------------------------
if st.session_state.final_destination:
    st.subheader("🗺️ Day-wise Itinerary")

    city_places = [
        p for p in places
        if p["city"].lower()
        == st.session_state.final_destination.lower()
    ]

    for i, p in enumerate(
        city_places[:st.session_state.days], 1
    ):
        st.markdown(f"### Day {i}: {p['name']}")
        st.write(p["type"])
        st.write(f"⭐ {p['rating']}")

# ----------------------------------
# BUDGET CALCULATION SECTION
# ----------------------------------
if st.session_state.flight_result:

    st.divider()
    st.subheader("💰 Budget Estimation")

    hotel_price = st.number_input(
        "Hotel price per night",
        500, step=500
    )

    if st.button("Estimate Budget"):
        flight_price = (
            st.session_state.flight_result
            ["flight"]["price"]
        )

        st.session_state.budget_result = (
            budget_estimation_tool.run({
                "flight_price": flight_price,
                "hotel_price_per_night": hotel_price,
                "number_of_days": st.session_state.days
            })
        )

# ----------------------------------
# FINAL BUDGET OUTPUT
# ----------------------------------
if st.session_state.budget_result:
    st.subheader("💵 Final Trip Cost")

    st.markdown(
        f"""
**Flight:** ₹{st.session_state.budget_result['flight_cost']}  
**Hotel:** ₹{st.session_state.budget_result['hotel_cost']}  
**Local:** ₹{st.session_state.budget_result['local_expenses']}  

### ✅ **Total: ₹{st.session_state.budget_result['total_cost']}**
"""
    )
