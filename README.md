# Travel Planner

Travel Planner is an agent-based web application built using Streamlit and LangChain that assists users in planning trips by dynamically retrieving travel-related information. The app uses an intelligent agent with tool-calling capabilities to search for flight details and present relevant results through an interactive interface. It is fully deployed on Streamlit Community Cloud and accessible via a public URL without requiring a local setup.

## Live Demo
👉 https://qebavqee6s6jfdakaidmkp.streamlit.app/

## Tech Stack
- Python
- Streamlit
- LangChain

## How It Works
- User chooses the source and destination cities
- The app will return the flight information (Airline, Duration, Departure Time, Price)
- Then the user selects the price range for the hotels (price per night)
- Then the app will return the hotel information (Name, Rating, Price)
- Then The app will return the locations to visit along with the weather forecast
- Then the user can select the budget range
- Then the app will return the entire budget for the trip
