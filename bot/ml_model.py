import joblib
import os

MODEL_PATH = "bot/model.joblib"

def predict_error_risk(indicators):
    if not os.path.exists(MODEL_PATH):
        return "LOW"  # fallback if model is not trained

    model = joblib.load(MODEL_PATH)
    X = [[
        indicators["ema20"],
        indicators["ema50"],
        indicators["rsi"],
        indicators["macd"]
    ]]
    prediction = model.predict(X)[0]
    return "HIGH" if prediction == 1 else "LOW"
