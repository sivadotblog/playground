"""Agent 1: Orchestrator Agent using Google ADK with Agent-as-Tool pattern"""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import AgentTool
from agent2_weather import create_weather_agent
from config import Config


def create_orchestrator_agent() -> Agent:
    """
    Create and configure the Orchestrator Agent using Google ADK.

    This agent coordinates with the Weather Service Agent using the
    Agent-as-Tool pattern, where the weather agent is called as a tool
    and its response is used to formulate the final user response.

    Returns:
        Configured Agent instance with weather agent as a tool
    """
    # Create the weather service agent
    weather_agent = create_weather_agent()

    # Create the orchestrator agent with weather agent as a tool
    orchestrator = Agent(
        model=LiteLlm(model=f"openai/{Config.OPENAI_MODEL}"),
        name="orchestrator",
        description=(
            "Orchestrator agent that handles user queries and delegates to "
            "specialized agents as needed. Primary capability: weather information."
        ),
        instruction="""
        You are a helpful orchestrator agent that assists users with their queries.
        
        When a user asks about weather:
        1. Use the weather_service tool to get the information
        2. The weather_service agent will handle the API call and return formatted data
        3. Present the response naturally to the user
        
        You have access to a weather service agent that can provide real-time 
        weather information for any location. Always delegate weather queries 
        to this specialized agent.
        
        Be conversational, helpful, and ensure users get accurate information.
        """,
        tools=[
            AgentTool(
                agent=weather_agent,
                skip_summarization=False,  # Let ADK summarize the response
            )
        ],
    )

    return orchestrator
