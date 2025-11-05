"""Main entry point for Google ADK agent-to-agent POC"""

import asyncio
import logging
import sys
from agent1_orchestrator import create_orchestrator_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)

# Constants
APP_NAME = "weather_agent_poc"
USER_ID = "demo_user"
SESSION_ID = "demo_session"


async def main():
    """Main execution function using Google ADK Runner"""

    print("\n" + "=" * 80)
    print("🚀 GOOGLE ADK: AGENT-TO-AGENT INTEGRATION POC")
    print("=" * 80 + "\n")

    logger.info("🎬 Starting Google ADK Agent-to-Agent POC")

    # Hardcoded user query for POC
    user_query = "what is the weather in mason ohio"

    print(f"📝 User Query: '{user_query}'\n")
    print("-" * 80 + "\n")

    try:
        # Initialize the orchestrator agent (which includes weather agent as tool)
        logger.info("🏗️  Creating orchestrator agent with ADK...")
        orchestrator = create_orchestrator_agent()
        
        # Set up ADK Session Service and Runner
        logger.info("📦 Initializing ADK Session Service...")
        session_service = InMemorySessionService()
        
        logger.info("🎯 Creating ADK Runner...")
        runner = Runner(
            agent=orchestrator,
            app_name=APP_NAME,
            session_service=session_service
        )
        
        # Create session
        logger.info(f"🔑 Creating session for user: {USER_ID}")
        session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID
        )

        print("-" * 80)
        print("🔄 AGENT INTERACTION (via ADK Runner)")
        print("-" * 80 + "\n")

        # Create user message
        content = types.Content(
            role="user",
            parts=[types.Part(text=user_query)]
        )

        # Run the agent asynchronously and stream events
        logger.info("▶️  Running orchestrator agent...")
        events = runner.run_async(
            user_id=USER_ID,
            session_id=session.id,
            new_message=content
        )

        # Process events and display agent responses
        async for event in events:
            # Log agent interactions
            if event.author:
                logger.info(f"📨 Event from: {event.author}")
            
            # Display text responses
            if event.content and event.content.parts:
                text_parts = [
                    part.text
                    for part in event.content.parts
                    if part.text
                ]
                if text_parts:
                    full_text = "".join(text_parts)
                    if full_text.strip():
                        print(f"[{event.author}]: {full_text}")
            
            # Check for final response
            if hasattr(event, 'is_final_response') and event.is_final_response():
                logger.info("✅ Received final response from agent")

        print("\n" + "-" * 80)
        logger.info("✅ POC demonstration completed successfully")

    except Exception as e:
        logger.error(f"❌ Error during execution: {str(e)}", exc_info=True)
        print(f"\n❌ Error: {str(e)}")
        return 1

    print("\n" + "=" * 80)
    print("🎉 GOOGLE ADK POC DEMONSTRATION COMPLETE")
    print("=" * 80 + "\n")
    
    print("📊 Key Features Demonstrated:")
    print("  ✅ Google ADK Agent framework")
    print("  ✅ Agent-as-Tool pattern (Agent 2 as tool for Agent 1)")
    print("  ✅ LiteLLM wrapper for OpenAI GPT-4")
    print("  ✅ Automatic FunctionTool wrapping")
    print("  ✅ ADK Runner and Session management")
    print("  ✅ Real-time weather API integration")
    print("  ✅ Comprehensive logging\n")

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
