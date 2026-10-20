
import re


def assess_message(message: str) -> dict:
    """Check a message for common scam warning signs."""

    text = message.lower()

    warning_signs = {
        "urgent_language": [
            "act now",
            "immediately",
            "urgent",
            "within 24 hours",
            "account will be blocked",
        ],
        "money_or_prize": [
            "you have won",
            "claim your prize",
            "free gift",
            "lottery winner",
            "cash reward",
        ],
        "sensitive_information": [
            "share your otp",
            "tell me your otp",
            "send your otp",
            "share your password",
            "confirm your pin",
        ],
        "suspicious_payment": [
            "pay processing fee",
            "pay registration fee",
            "send money to receive",
            "pay to claim",
        ],
    }

    findings = []

    for category, phrases in warning_signs.items():
        for phrase in phrases:
            if phrase in text:
                findings.append({
                    "category": category,
                    "evidence": phrase,
                })

    if re.search(r"https?://|www\.", text):
        findings.append({
            "category": "contains_link",
            "evidence": "The message contains a web link.",
        })

    if any(item["category"] == "sensitive_information"
           for item in findings):
        risk_level = "high"
    elif len(findings) >= 2:
        risk_level = "high"
    elif len(findings) == 1:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "risk_level": risk_level,
        "warning_count": len(findings),
        "warning_signs": findings,
        "message": (
            "Warning signs detected. Verify independently."
            if findings
            else "No listed warning signs detected. "
                 "This does not guarantee the message is safe."
        ),
    }


def next_steps(result: dict) -> list[str]:
    """Suggest practical safety steps based on detected warning signs."""

    steps = []

    categories = {
        item["category"]
        for item in result.get("warning_signs", [])
    }

    if "sensitive_information" in categories:
        steps.append(
            "Never share your OTP, password, or PIN with anyone."
        )

    if "contains_link" in categories:
        steps.append(
            "Avoid opening suspicious links. Visit the official "
            "website or app independently."
        )

    if "suspicious_payment" in categories or "money_or_prize" in categories:
        steps.append(
            "Do not pay unexpected fees to claim prizes or receive money."
        )

    if "urgent_language" in categories:
        steps.append(
            "Pause and verify the request using an official contact number."
        )

    if not steps:
        steps.append(
            "No listed warning signs were found. Verify the sender "
            "before sharing information or making payments."
        )

    steps.append(
        "If you suspect fraud, preserve the message and report it "
        "through an appropriate official channel."
    )

    return steps
