import re


WARNING_PHRASES = {
    "urgent_language": [
        "act now", "immediately", "urgent", "within 24 hours",
        "account will be blocked", "account will be suspended",
        "last chance", "final warning",
    ],
    "money_or_prize": [
        "you have won", "claim your prize", "free gift",
        "lottery winner", "cash reward", "you are a winner",
        "claim your reward", "processing fee to claim",
        "pay a processing fee", "prize money",
    ],
    "sensitive_information": [
        "share your otp", "tell me your otp", "send your otp",
        "share your password", "confirm your pin",
        "send me your password", "share your pin", "provide your otp",
    ],
    "suspicious_payment": [
        "pay processing fee", "pay a processing fee",
        "pay registration fee", "send money to receive",
        "pay to claim", "pay a fee to release",
        "transfer money to unlock", "pay a processing fee to claim",
    ],
    "account_threat": [
        "update your kyc immediately", "kyc will expire",
        "verify your bank account", "account suspended",
        "account has been blocked", "reactivate your account",
    ],
    "suspicious_installation": [
        "install this apk", "install this app to receive",
        "install remote access", "download anydesk",
        "download teamviewer",
    ],
}

URL_PATTERN = re.compile(r"(?:https?://|www\.)[^\s]+", re.IGNORECASE)


def assess_message(message: str) -> dict:
    """Identify common scam warning signs using transparent rules."""
    if not isinstance(message, str) or not message.strip():
        raise ValueError("Please provide a non-empty message.")

    text = message.lower().strip()
    findings = []

    for category, phrases in WARNING_PHRASES.items():
        for phrase in phrases:
            if phrase in text:
                findings.append({
                    "category": category,
                    "evidence": phrase,
                })

    has_url = bool(URL_PATTERN.search(text))

    if has_url:
        findings.append({
            "category": "contains_link",
            "evidence": "The message contains a web link.",
        })

    categories = {item["category"] for item in findings}
    scam_categories = categories - {"contains_link"}

    # Prize/payment combinations are especially suspicious.
    prize_payment_combo = (
        "money_or_prize" in scam_categories
        and "suspicious_payment" in scam_categories
    )

    if (
        "sensitive_information" in scam_categories
        or "suspicious_installation" in scam_categories
        or prize_payment_combo
        or len(scam_categories) >= 2
    ):
        risk_level = "high"
    elif len(scam_categories) == 1:
        risk_level = "medium"
    else:
        risk_level = "low"

    if scam_categories:
        result_message = (
            "Potential scam warning signs detected. "
            "Verify the sender and request independently."
        )
    elif has_url:
        result_message = (
            "A link was found, but a link alone does not prove "
            "a scam. Check the destination before opening it."
        )
    else:
        result_message = (
            "No listed warning signs detected. "
            "This does not guarantee the message is safe."
        )

    return {
        "risk_level": risk_level,
        "warning_count": len(findings),
        "warning_signs": findings,
        "message": result_message,
    }


def next_steps(result: dict) -> list[str]:
    """Return practical safety advice based on detected findings."""
    steps = []
    categories = {
        item["category"]
        for item in result.get("warning_signs", [])
    }

    if "sensitive_information" in categories:
        steps.append("Never share your OTP, password, or PIN with anyone.")

    if "contains_link" in categories:
        steps.append(
            "Check the destination carefully. Open the official website "
            "or app independently when in doubt."
        )

    if (
        "suspicious_payment" in categories
        or "money_or_prize" in categories
    ):
        steps.append(
            "Do not pay unexpected fees to claim prizes or receive money."
        )

    if (
        "urgent_language" in categories
        or "account_threat" in categories
    ):
        steps.append(
            "Pause and verify the request using an official contact number."
        )

    if "suspicious_installation" in categories:
        steps.append(
            "Do not install unknown apps or grant remote access "
            "to someone who contacted you unexpectedly."
        )

    if not steps:
        steps.append(
            "No listed scam indicators were found. Verify the sender "
            "before sharing information or making payments."
        )

    steps.append(
        "If you suspect fraud in India, call 1930 or report at "
        "https://cybercrime.gov.in/"
    )

    return steps