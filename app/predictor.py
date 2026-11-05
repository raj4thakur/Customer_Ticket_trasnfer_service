
import numpy as np

# def predict_ticket(subject, body, artifacts):
#     model = artifacts["model"]
#     tokenizer = artifacts["tokenizer"]
#     category_encoder = artifacts["category_encoder"]
#     urgency_encoder = artifacts["urgency_encoder"]
#     max_text_len = artifacts["max_text_len"]
#     padding = artifacts["padding"]

#     text = [str(subject) + " " + str(body)]

#     sequence = tokenizer.texts_to_sequences(text)
#     padded_sequence = pad_sequences(sequence,maxlen=max_text_len,padding=padding)
    
#     category_pred, urgency_pred = model.predict(padded_sequence,verbose=0)

#     category_id = int(np.argmax(category_pred[0]))
#     urgency_id = int(np.argmax(urgency_pred[0]))

#     # Convert indexes back to original labels
#     category_name = category_encoder.inverse_transform([category_id])[0]

#     urgency_name = urgency_encoder.inverse_transform([urgency_id])[0]

 
#     category_confidence = float(category_pred[0][category_id])
#     urgency_confidence = float(urgency_pred[0][urgency_id])

#     return {
#         "category": str(category_name),
#         "urgency": str(urgency_name),
#         "category_confidence": round(category_confidence, 4),
#         "urgency_confidence": round(urgency_confidence, 4)
#     }


import re

def preprocess_text(subject, body):

    text = f"{subject} {body}"

    text = text.lower()

    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"www\S+", " ", text)

    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text

import numpy as np

def predict_ticket(subject, body, artifacts):

    model = artifacts["model"]

    tfidf = artifacts["vectorizer"]

    category_encoder = artifacts["category_encoder"]

    urg_map_encoder={0:'Low',1:"Medium",2:"High"}

    text = preprocess_text(subject, body)

    X = tfidf.transform([text])

    preds = model.predict(X)

    category_id = int(preds[0][0])
    urgency_id = int(preds[0][1])

    category_name = category_encoder.inverse_transform(
        [category_id]
    )[0]

    urgency_name = urg_map_encoder[urgency_id]

    # confidence scores
    category_probs = model.estimators_[0].predict_proba(X)[0]
    urgency_probs = model.estimators_[1].predict_proba(X)[0]

    category_confidence = float(np.max(category_probs))
    urgency_confidence = float(np.max(urgency_probs))

    return {
        "category": str(category_name),
        "urgency": str(urgency_name),
        "category_confidence": round(category_confidence, 4),
        "urgency_confidence": round(urgency_confidence, 4)
    }