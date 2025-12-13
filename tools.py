from livekit.agents import function_tool


@function_tool
async def get_weather(city: str) -> dict:
    """
    Mock function to get weather data for a city.
    In a real application, this would call a weather API.

    Args:
        city: Name of the city in Morocco

    Returns:
        Dictionary containing weather information
    """
    # Mock weather data for Moroccan cities
    weather_data = {
        "casablanca": {
            "city": "الدار البيضاء (Casablanca)",
            "temperature": 22,
            "condition": "مشمس (Sunny)",
            "humidity": 65,
            "wind_speed": 15,
        },
        "rabat": {
            "city": "الرباط (Rabat)",
            "temperature": 20,
            "condition": "غيوم خفيفة (Partly Cloudy)",
            "humidity": 70,
            "wind_speed": 12,
        },
        "marrakech": {
            "city": "مراكش (Marrakech)",
            "temperature": 28,
            "condition": "مشمس (Sunny)",
            "humidity": 45,
            "wind_speed": 8,
        },
        "fes": {
            "city": "فاس (Fes)",
            "temperature": 24,
            "condition": "صافي (Clear)",
            "humidity": 55,
            "wind_speed": 10,
        },
        "tangier": {
            "city": "طنجة (Tangier)",
            "temperature": 19,
            "condition": "غيوم (Cloudy)",
            "humidity": 75,
            "wind_speed": 18,
        },
        "agadir": {
            "city": "أكادير (Agadir)",
            "temperature": 25,
            "condition": "مشمس (Sunny)",
            "humidity": 60,
            "wind_speed": 14,
        },
    }

    # Normalize city name
    city_normalized = city.lower().strip()

    # Return weather data or default
    return weather_data.get(
        city_normalized,
        {
            "city": city,
            "temperature": 23,
            "condition": "مشمس (Sunny)",
            "humidity": 60,
            "wind_speed": 12,
        },
    )
