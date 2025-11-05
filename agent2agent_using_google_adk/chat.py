"""Interactive CLI Chat with Google ADK Agent-to-Agent Integration"""

import asyncio
import logging
import sys
from agent1_orchestrator import create_orchestrator_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Configure logging
logging.basicConfig(
    level=logging.WARNING,  # Only show warnings and errors for cleaner chat
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)

# Constants
APP_NAME = "weather_agent_poc"
USER_ID = "demo_user"
SESSION_ID = "chat_session"


class InteractiveChat:
    """Interactive chat interface using Google ADK"""

    def __init__(self):
        self.runner = None
        self.session_service = None
        self.session = None

    async def initialize(self):
        """Initialize the ADK components"""
        print("\n" + "=" * 80)
        print("🤖 GOOGLE ADK INTERACTIVE AGENT CHAT")
        print("=" * 80)
        print("\nInitializing agents...")

        # Create orchestrator agent with weather agent as tool
        orchestrator = create_orchestrator_agent()

        # Set up session service and runner
        self.session_service = InMemorySessionService()
        self.runner = Runner(
            agent=orchestrator, app_name=APP_NAME, session_service=self.session_service
        )

        # Create session
        self.session = await self.session_service.create_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
        )

        print("✅ Agents ready!")
        print("\n" + "-" * 80)
        print("💬 Chat Tips:")
        print("  • Ask about weather: 'what's the weather in New York?'")
        print("  • Multi-turn: Agents remember conversation context")
        print("  • Type 'exit', 'quit', or press Ctrl+C to end")
        print("-" * 80 + "\n")

    async def send_message(self, user_input: str):
        """Send a message to the agent and display response"""
        # Create user message
        content = types.Content(role="user", parts=[types.Part(text=user_input)])

        # Run agent and stream events
        events = self.runner.run_async(
            user_id=USER_ID, session_id=self.session.id, new_message=content
        )

        print("🤖 Agent: ", end="", flush=True)

        response_text = ""
        async for event in events:
            # Display text responses as they come
            if event.content and event.content.parts:
                text_parts = [part.text for part in event.content.parts if part.text]
                if text_parts:
                    chunk = "".join(text_parts)
                    if chunk.strip() and chunk not in response_text:
                        print(chunk, end="", flush=True)
                        response_text += chunk

        print("\n")  # New line after response

    async def chat_loop(self):
        """Main interactive chat loop"""
        await self.initialize()

        while True:
            try:
                # Get user input
                user_input = input("👤 You: ").strip()

                # Check for exit commands
                if user_input.lower() in ["exit", "quit", "bye", "q"]:
                    print("\n👋 Goodbye! Thanks for chatting.\n")
                    break

                # Skip empty input
                if not user_input:
                    continue

                # Send message to agent
                await self.send_message(user_input)

            except KeyboardInterrupt:
                print("\n\n👋 Chat interrupted. Goodbye!\n")
                break
            except Exception as e:
                logger.error(f"Error in chat loop: {e}", exc_info=True)
                print(f"❌ Error: {e}\n")
                print("Let's try again...\n")


async def main():
    """Main entry point for interactive chat"""
    chat = InteractiveChat()
    await chat.chat_loop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!\n")
        sys.exit(0)
