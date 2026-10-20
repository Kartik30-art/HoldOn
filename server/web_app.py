import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

from server.ml_engine import predict_message


app = FastAPI(title="HoldOn Scam Checker")

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

MCP_URL = "http://127.0.0.1:8000/mcp"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static",
)


class MessageRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/analyze")
async def analyze_message(request: MessageRequest):
    message = request.message.strip()

    if not message:
        raise HTTPException(
            status_code=400,
            detail="Please enter a message to analyze.",
        )

    try:
        async with streamablehttp_client(MCP_URL) as (
            read_stream,
            write_stream,
            _,
        ):
            async with ClientSession(
                read_stream, write_stream
            ) as session:
                await session.initialize()

                detection = await session.call_tool(
                    "check_suspicious_message",
                    {"message": message},
                )

                if detection.isError:
                    raise RuntimeError(
                        "The scam-detection MCP tool failed."
                    )

                detection_text = "".join(
                    item.text
                    for item in detection.content
                    if hasattr(item, "text")
                )

                result = json.loads(detection_text)

                if not isinstance(result, dict):
                    raise RuntimeError(
                        "The detection tool returned invalid data."
                    )

                # Normalize warning signs and calculate the count
                # from the exact list sent to the frontend.
                warnings = result.get("warning_signs", [])

                if not isinstance(warnings, list):
                    warnings = []

                result["warning_signs"] = warnings
                result["warning_count"] = len(warnings)

                advice = await session.call_tool(
                    "get_safe_next_steps",
                    {"message": message},
                )

                if advice.isError:
                    raise RuntimeError(
                        "The safety-advice MCP tool failed."
                    )

                advice_text = "\n".join(
                    item.text
                    for item in advice.content
                    if hasattr(item, "text")
                )

                try:
                    next_steps = json.loads(advice_text)

                    if not isinstance(next_steps, list):
                        next_steps = [
                            line.strip()
                            for line in advice_text.splitlines()
                            if line.strip()
                        ]

                except json.JSONDecodeError:
                    next_steps = [
                        line.strip()
                        for line in advice_text.splitlines()
                        if line.strip()
                    ]

                result["next_steps"] = next_steps

                # Experimental ML prediction.
                try:
                    result["ml_analysis"] = predict_message(message)
                    result["ml_analysis"]["available"] = True

                except Exception as ml_error:
                    print(
                        f"Experimental ML model error: {ml_error}"
                    )

                    result["ml_analysis"] = {
                        "available": False,
                        "experimental": True,
                        "message": (
                            "ML prediction is temporarily unavailable."
                        ),
                    }

                return result

    except Exception as error:
        print(f"MCP connection error: {error}")

        raise HTTPException(
            status_code=503,
            detail=(
                "HoldOn could not complete the analysis. "
                "Check that the MCP server is running."
            ),
        ) from error
