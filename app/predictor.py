
import numpy as np

from tensorflow.keras.preprocessing.sequence import pad_sequences


def predict_ticket(subject, body, artifacts):
    model = artifacts["model"]
    tokenizer = artifacts["tokenizer"]
    category_encoder = artifacts["category_encoder"]
    urgency_encoder = artifacts["urgency_encoder"]
    max_text_len = artifacts["max_text_len"]
    padding = artifacts["padding"]

    text = [str(subject) + " " + str(body)]

    sequence = tokenizer.texts_to_sequences(text)
    padded_sequence = pad_sequences(sequence,maxlen=max_text_len,padding=padding)
    
    category_pred, urgency_pred = model.predict(padded_sequence,verbose=0)

    category_id = int(np.argmax(category_pred[0]))
    urgency_id = int(np.argmax(urgency_pred[0]))

    # Convert indexes back to original labels
    category_name = category_encoder.inverse_transform([category_id])[0]

    urgency_name = urgency_encoder.inverse_transform([urgency_id])[0]

 
    category_confidence = float(category_pred[0][category_id])
    urgency_confidence = float(urgency_pred[0][urgency_id])

    return {
        "category": str(category_name),
        "urgency": str(urgency_name),
        "category_confidence": round(category_confidence, 4),
        "urgency_confidence": round(urgency_confidence, 4)
    }
