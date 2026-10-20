
from pathlib import Path

from joblib import load


PROJECT_DIR = Path(__file__).resolve().parent.parent
MODEL_FILE = PROJECT_DIR / "models" / "holdon_text_model.joblib"

_model = None


def get_model():
    """Load the trained model once, when first needed."""
    global _model

    if _model is None:
        if not MODEL_FILE.exists():
            raise FileNotFoundError(
                f"Trained model not found: {MODEL_FILE}"
            )

        _model = load(MODEL_FILE)

    return _model


def predict_message(message: str) -> dict:
    """Return the model's text classification."""
    if not isinstance(message, str) or not message.strip():
        raise ValueError("Please provide a non-empty message.")

    model = get_model()
    prediction = model.predict([message])[0]

    probabilities = model.predict_proba([message])[0]
    classes = list(model.classes_)
    confidence = float(probabilities[classes.index(prediction)])

    return {
        "prediction": str(prediction),
        "confidence": round(confidence, 4),
        "model": "TF-IDF + Logistic Regression",
        "experimental": True,
    }
