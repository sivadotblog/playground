"""Agent 2: Weather Service Agent using Google ADK"""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from tools.weather_tools import get_weather
from config import Config


def create_weather_agent() -> Agent:
    """
    Create and configure the Weather Service Agent using Google ADK.

    This agent provides weather information using real-time API calls.
    The get_weather function is automatically wrapped as a FunctionTool by ADK.

    Returns:
        Configured Agent instance with weather capabilities
    """
    weather_agent = Agent(
        model=LiteLlm(model=f"openai/{Config.OPENAI_MODEL}"),
        name="weather_service",
        description=(
            "Weather service agent that provides current weather information "
            "for any location worldwide. Uses real-time weather data from wttr.in API."
        ),
        instruction="""
        You are a weather information specialist. Your job is to provide accurate,
        current weather information for requested locations.
        
        When asked about weather:
        1. Use the get_weather tool to fetch real-time data
        2. Present the information clearly and conversationally
        3. Include key details like temperature, conditions, and location
        4. If there's an error, explain it clearly to the user
        
        Always be helpful and accurate with weather information.
        """,
        tools=[get_weather],  # ADK automatically wraps this as FunctionTool
    )

    return weather_agent
