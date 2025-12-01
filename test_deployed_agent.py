"""Test script for the deployed A2A agent on Cloud Run."""

import asyncio
import os
import sys
import uuid
from typing import List, cast

import httpx
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    Message,
    MessageSendParams,
    Part,
    Role,
    SendMessageRequest,
    TextPart,
)


async def test_agent(agent_url: str) -> None:
    """
    Test the deployed A2A agent.
    
    Args:
        agent_url: The Cloud Run service URL (e.g., https://agent2agent-dev-xxx.run.app)
    """
    print(f" Testing A2A Agent at: {agent_url}")
    print("=" * 60)
    
    async with httpx.AsyncClient(timeout=30.0) as httpx_client:
        # Step 1: Fetch agent card
        print("\n📋 Step 1: Fetching agent card...")
        try:
            resolver = A2ACardResolver(httpx_client=httpx_client, base_url=agent_url)
            agent_card = await resolver.get_agent_card("/.well-known/agent.json")
            print(f" Agent card fetched successfully!")
            print(f"   Agent Name: {agent_card.name}")
            print(f"   Description: {agent_card.description}")
            print(f"   Version: {agent_card.version}")
            print(f"   Skills: {len(agent_card.skills)} available")
            for skill in agent_card.skills:
                print(f"      - {skill.name}: {skill.description}")
        except Exception as e:
            print(f" Failed to fetch agent card: {e}")
            return
        
        # Step 2: Initialize A2A client
        print("\n Step 2: Initializing A2A client...")
        try:
            client = A2AClient(
                httpx_client=httpx_client,
                agent_card=agent_card,
            )
            print(" Client initialized successfully!")
        except Exception as e:
            print(f" Failed to initialize client: {e}")
            return
        
        # Step 3: Send a test message
        print("\n💬 Step 3: Sending test message...")
        test_messages = [
            "Hello, how are you?",
            "What can you do?",
            "Tell me a greeting",
        ]
        
        for test_text in test_messages:
            print(f"\n   Sending: '{test_text}'")
            try:
                part: Part = cast(Part, TextPart(text=test_text))
                parts: List[Part] = [part]
                
                message = Message(
                    role=Role.user,
                    message_id=str(uuid.uuid4()),
                    parts=parts,
                )
                
                request = SendMessageRequest(
                    id=str(uuid.uuid4()),
                    params=MessageSendParams(message=message),
                )
                
                response = await client.send_message(request)
                
                print(f"    Response received:")
                # Extract text from response
                if response.result and response.result.message:
                    for part in response.result.message.parts:
                        if hasattr(part, 'text'):
                            print(f"      {part.text}")
                else:
                    print(f"      {response.model_dump_json(indent=2)}")
                    
            except Exception as e:
                print(f"    Failed to send message: {e}")
        
        print("\n" + "=" * 60)
        print("🎉 Testing complete!")


async def main() -> None:
    """Main entry point."""
    # Get agent URL from environment or command line
    agent_url = os.getenv("AGENT_URL")
    
    if len(sys.argv) > 1:
        agent_url = sys.argv[1]
    
    if not agent_url:
        print(" Error: No agent URL provided!")
        print("\nUsage:")
        print("  python test_deployed_agent.py https://your-service-url.run.app")
        print("  OR")
        print("  export AGENT_URL=https://your-service-url.run.app")
        print("  python test_deployed_agent.py")
        sys.exit(1)
    
    # Remove trailing slash if present
    agent_url = agent_url.rstrip("/")
    
    await test_agent(agent_url)


if __name__ == "__main__":
    asyncio.run(main())
