
import json
import joblib
import tensorflow as tf

from pathlib import Path
from tensorflow.keras.preprocessing.text import tokenizer_from_json


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Artifacts directory
ARTIFACTS_DIR = BASE_DIR / "artifacts"


def load_artifacts():
    """Load the trained model and preprocessing artifacts."""

    model_path = ARTIFACTS_DIR / "ticket_classifier.keras"
    tokenizer_path = ARTIFACTS_DIR / "tokenizer.json"
    category_encoder_path = ARTIFACTS_DIR / "category_encoder.pkl"
    urgency_encoder_path = ARTIFACTS_DIR / "urgency_encoder.pkl"
    config_path = ARTIFACTS_DIR / "config.json"

    # Load trained TensorFlow model
    model = tf.keras.models.load_model(model_path)

    # Load tokenizer
    with open(tokenizer_path, "r", encoding="utf-8") as file:
        tokenizer = tokenizer_from_json(file.read())

    # Load label encoders
    category_encoder = joblib.load(category_encoder_path)
    urgency_encoder = joblib.load(urgency_encoder_path)

    # Load configuration
    with open(config_path, "r", encoding="utf-8") as file:
        config = json.load(file)

    return {
        "model": model,
        "tokenizer": tokenizer,
        "category_encoder": category_encoder,
        "urgency_encoder": urgency_encoder,
        "max_text_len": config["max_text_len"],
        "padding": config.get("padding", "post")
    }
