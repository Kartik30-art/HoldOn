
import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def main():
    async with streamablehttp_client(
        "http://127.0.0.1:8000/mcp"
    ) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            print("Testing scam detection...")

            result = await session.call_tool(
                "check_suspicious_message",
                {
                    "message": (
                        "You have won a prize! "
                        "Pay processing fee immediately."
                    )
                },
            )

            for item in result.content:
                if hasattr(item, "text"):
                    print(item.text)

            print("\nTesting safety advice...")

            advice = await session.call_tool(
                "get_safe_next_steps",
                {
                    "message": (
                        "You have won a prize! "
                        "Pay processing fee immediately."
                    )
                },
            )

            for item in advice.content:
                if hasattr(item, "text"):
                    print(item.text)

            print("\nMCP TOOL EXECUTION TEST FINISHED")


asyncio.run(main())
