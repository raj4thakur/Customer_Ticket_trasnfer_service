
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

    model_path = ARTIFACTS_DIR / "model.pkl"
    vectorizer_path = ARTIFACTS_DIR / "tfidf.pkl"
    category_encoder_path = ARTIFACTS_DIR / "category_encoder.pkl"

    model = joblib.load(model_path)

    vectorizer = joblib.load(vectorizer_path)

    category_encoder = joblib.load(category_encoder_path)

    return {
        "model": model,
        "category_encoder": category_encoder,
        "vectorizer": vectorizer
    }