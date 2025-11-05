import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration management for the agent POC"""

    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # Agent Configuration
    AGENT1_NAME = "Orchestrator Agent"
    AGENT2_NAME = "Weather Service Agent"

    # Weather API Configuration
    WEATHER_API_URL = "https://wttr.in/{location}?format=j1"

    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required in .env file")
        return True


# Validate configuration on import
Config.validate()
