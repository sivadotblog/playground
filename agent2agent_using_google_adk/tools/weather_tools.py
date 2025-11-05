"""Weather tools for ADK agent - Pure Python functions with type hints"""

import httpx
from typing import Dict, Any


async def get_weather(location: str) -> Dict[str, Any]:
    """
    Get current weather information for a specified location.

    This function fetches real-time weather data from the wttr.in API.
    It provides detailed information including temperature, conditions,
    humidity, and wind speed.

    Args:
        location: City name or location (e.g., 'Mason, Ohio', 'New York')

    Returns:
        Dictionary containing weather information with keys:
        - location: The requested location
        - area_name: Standardized area name
        - country: Country name
        - temperature_f: Temperature in Fahrenheit
        - temperature_c: Temperature in Celsius
        - condition: Weather condition description
        - humidity: Humidity percentage
        - wind_speed_mph: Wind speed in miles per hour
        - feels_like_f: Feels like temperature in Fahrenheit
        - observation_time: Time of observation

        If an error occurs, returns a dictionary with an 'error' key.
    """
    try:
        # Clean and format the location
        location_clean = location.strip().replace(" ", "+")
        url = f"https://wttr.in/{location_clean}?format=j1"

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()

            data = response.json()

            # Extract relevant weather information
            current = data.get("current_condition", [{}])[0]
            location_info = data.get("nearest_area", [{}])[0]

            weather_data = {
                "location": location,
                "area_name": location_info.get("areaName", [{}])[0].get(
                    "value", location
                ),
                "country": location_info.get("country", [{}])[0].get(
                    "value", "Unknown"
                ),
                "temperature_f": current.get("temp_F", "N/A"),
                "temperature_c": current.get("temp_C", "N/A"),
                "condition": current.get("weatherDesc", [{}])[0].get("value", "N/A"),
                "humidity": current.get("humidity", "N/A"),
                "wind_speed_mph": current.get("windspeedMiles", "N/A"),
                "feels_like_f": current.get("FeelsLikeF", "N/A"),
                "observation_time": current.get("observation_time", "N/A"),
            }

            return weather_data

    except httpx.HTTPError as e:
        return {
            "error": f"Failed to fetch weather data: {str(e)}",
            "location": location,
        }
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}", "location": location}
