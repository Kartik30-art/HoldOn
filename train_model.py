
import csv
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


PROJECT_DIR = Path(__file__).resolve().parent
DATA_FILE = PROJECT_DIR / "data" / "messages.csv"
MODEL_FILE = PROJECT_DIR / "models" / "holdon_text_model.joblib"


def load_messages():
    messages = []
    labels = []

    with DATA_FILE.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            message = row["message"].strip()
            label = row["label"].strip().lower()

            if message and label in {"scam", "legitimate"}:
                messages.append(message)
                labels.append(label)

    if len(set(labels)) < 2:
        raise ValueError(
            "The dataset must contain both scam and legitimate messages."
        )

    if len(messages) < 10:
        raise ValueError(
            "Please add more labelled examples before training."
        )

    return messages, labels


def main():
    messages, labels = load_messages()

    model = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                ngram_range=(1, 2),
                strip_accents="unicode"
            )
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced",
                random_state=42
            )
        )
    ])

    model.fit(messages, labels)

    MODEL_FILE.parent.mkdir(parents=True, exist_ok=True)

    from joblib import dump
    dump(model, MODEL_FILE)

    print("Training completed.")
    print(f"Training examples: {len(messages)}")
    print(f"Scam examples: {labels.count('scam')}")
    print(f"Legitimate examples: {labels.count('legitimate')}")
    print(f"Saved model to: {MODEL_FILE}")


if __name__ == "__main__":
    main()
