

def calculate_budget(
    flight_price: int,
    hotel_price_per_night: int,
    number_of_days: int,
    daily_expense: int = 1500
):

# This function will create a logic to calculate total expense, we will assign an default value to daily_expense (1500)
    
    """
    Calculates total trip budget.
    """

    hotel_nights = number_of_days - 1 # here we will fetch the number of nights stayed at the hotel
    hotel_cost = hotel_price_per_night * hotel_nights # here we will calculate the total hotel expense
    local_expenses = daily_expense * number_of_days # here we will calculate the daily expense
    total_cost = flight_price + hotel_cost + local_expenses # here we will calculate the total budget

    return {
        "flight_cost": flight_price,
        "hotel_cost": hotel_cost,
        "local_expenses": local_expenses,
        "total_cost": total_cost
    }
# This function will return a structured output, including flight, hotel, local and total costs



# now we will wrapp this logic inside an lang chain framework, as a tool

from langchain.tools import tool
@tool
def budget_estimation_tool(
    flight_price: int,
    hotel_price_per_night: int,
    number_of_days: int
):
    """
    Calculates total trip budget including flight, hotel, and daily expenses.
    """
    daily_expense = 1500

    hotel_nights = number_of_days - 1
    hotel_cost = hotel_price_per_night * hotel_nights
    local_expenses = daily_expense * number_of_days
    total_cost = flight_price + hotel_cost + local_expenses

    return {
        "flight_cost": flight_price,
        "hotel_cost": hotel_cost,
        "local_expenses": local_expenses,
        "total_cost": total_cost
    }



# Here we can test the tool
output = budget_estimation_tool.run({
    "flight_price": 6500,
    "hotel_price_per_night": 3000,
    "number_of_days": 3
})

print(output)
