
import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def main():
    url = "http://127.0.0.1:8000/mcp"

    async with streamablehttp_client(url) as (
        read_stream,
        write_stream,
        _,
    ):
        async with ClientSession(
            read_stream, write_stream
        ) as session:
            await session.initialize()

            message = (
                "Your bank account will be blocked. "
                "Share your OTP immediately: http://example.com"
            )

            print("\nTESTING SAFE NEXT STEPS:\n")

            result = await session.call_tool(
                "get_safe_next_steps",
                {"message": message},
            )

            for item in result.content:
                if hasattr(item, "text"):
                    print(item.text)


if __name__ == "__main__":
    asyncio.run(main())
