from fastapi import FastAPI
from quantum_sim.bb84 import simulate_bb84
from features.extract_features import extract_features
from ml_model.detector import detect

app = FastAPI()

@app.get("/detect")
def detect_channel(attack: bool = False):
    a, b = simulate_bb84(eavesdrop=attack)
    features = extract_features(a, b)
    score, attacked = detect(features)

    return {
        "QBER": features[0],
        "Entropy": features[1],
        "AnomalyScore": score,
        "Eavesdropping": attacked
    }
