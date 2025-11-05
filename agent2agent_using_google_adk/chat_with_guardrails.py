"""Interactive CLI Chat with Google ADK Agent-to-Agent Integration and Nemo Guardrails"""

import asyncio
import logging
import sys
from agent1_orchestrator import create_orchestrator_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Nemo Guardrails imports
from nemoguardrails import LLMRails, RailsConfig

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
    """Interactive chat interface using Google ADK with Nemo Guardrails"""

    def __init__(self):
        self.runner = None
        self.session_service = None
        self.session = None
        self.rails = None

    async def initialize(self):
        """Initialize the ADK components and Nemo Guardrails"""
        print("\n" + "=" * 80)
        print("🤖 GOOGLE ADK INTERACTIVE AGENT CHAT WITH NEMO GUARDRAILS")
        print("=" * 80)
        print("\nInitializing agents and guardrails...")

        # Initialize Nemo Guardrails
        config = RailsConfig.from_path("./config")
        self.rails = LLMRails(config)
        print("✅ Guardrails loaded from ./config")

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
        print("  • 🛡️ Content safety guardrails are active")
        print("  • Type 'exit', 'quit', or press Ctrl+C to end")
        print("-" * 80 + "\n")

    async def check_input_safety(self, user_input: str) -> tuple[bool, str]:
        """
        Check if user input is safe using Nemo Guardrails
        Returns: (is_safe, response_text)
        """
        try:
            messages = [{"role": "user", "content": user_input}]

            # Check input through guardrails
            response_chunks = []
            async for chunk in self.rails.stream_async(messages=messages):
                response_chunks.append(chunk)

            response_text = "".join(response_chunks)

            # If response indicates blocked content, it's unsafe
            # Nemo guardrails will return a safety message if content is unsafe
            if "cannot" in response_text.lower() or "unsafe" in response_text.lower():
                return False, response_text

            return True, response_text

        except Exception as e:
            logger.error(f"Error checking input safety: {e}", exc_info=True)
            # On error, allow the message but log it
            return True, ""

    async def send_message(self, user_input: str):
        """Send a message to the agent and display response with guardrails"""

        # Check input safety with guardrails
        is_safe, safety_response = await self.check_input_safety(user_input)

        if not is_safe:
            print("🛡️ Guardrails: ", end="", flush=True)
            print(safety_response)
            print()
            return

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

        # Check output safety with guardrails
        if response_text.strip():
            output_safe = await self.check_output_safety(user_input, response_text)
            if not output_safe:
                print("\n🛡️ [Response was filtered by guardrails]")

        print("\n")  # New line after response

    async def check_output_safety(self, user_input: str, bot_response: str) -> bool:
        """
        Check if bot output is safe using Nemo Guardrails
        Returns: True if safe, False if unsafe
        """
        try:
            # Create conversation messages for output check
            messages = [
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": bot_response},
            ]

            # Check output through guardrails
            response_chunks = []
            async for chunk in self.rails.stream_async(messages=messages):
                response_chunks.append(chunk)

            response_text = "".join(response_chunks)

            # If response indicates blocked content, it's unsafe
            if "cannot" in response_text.lower() or "unsafe" in response_text.lower():
                return False

            return True

        except Exception as e:
            logger.error(f"Error checking output safety: {e}", exc_info=True)
            # On error, allow the response but log it
            return True

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

                # Send message to agent with guardrails
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
