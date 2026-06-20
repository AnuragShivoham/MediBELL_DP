import os
import sys
import joblib
import pandas as pd
import numpy as np

# Add project root to path
sys.path.append(os.getcwd())

from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import SGDClassifier
from utils.preprocessing import apply_dp

def load_and_predict():
    print("\n" + "="*40)
    print("MEDIBELL ADVANCED PREDICTOR (DP + FL)")
    print("="*40)

    # 1. Load Model Data
    model_paths = ["fl_advanced/global_model_advanced.pkl", "fl_advanced/production_global_model.pkl"]
    data = None
    for path in model_paths:
        try:
            data = joblib.load(path)
            print(f"Loaded model from: {path}")
            break
        except Exception:
            continue

    if data is None:
        print("Error: Model file not found. Run simulation first.")
        return

    weights = data['weights']
    model_type = data['model_type']
    scaler = data['scaler']
    le = data['le']

    # 2. Re-initialize model architecture
    if model_type == "mlp":
        hidden_sizes = tuple(coef.shape[1] for coef in weights['coefs'][:-1])
        model = MLPClassifier(hidden_layer_sizes=hidden_sizes)
        # Fit dummy data to initialize scikit-learn internals
        n_features = weights['coefs'][0].shape[0]
        dummy_X = np.zeros((len(weights['classes']), n_features))
        dummy_y = weights['classes']
        model.fit(dummy_X, dummy_y)
        # Overwrite with aggregated weights
        model.coefs_ = weights['coefs']
        model.intercepts_ = weights['intercepts']
    else:
        model = SGDClassifier(loss='log_loss')
        # Fit dummy data to initialize scikit-learn internals
        n_features = weights['coef'].shape[1]
        dummy_X = np.zeros((len(weights['classes']), n_features))
        dummy_y = weights['classes']
        model.fit(dummy_X, dummy_y)
        # Overwrite with aggregated weights
        model.coef_ = weights['coef']
        model.intercept_ = weights['intercept']
    
    model.classes_ = weights['classes']

    # 3. Interactive Input
    print(f"\n[Model: {model_type.upper()} Mode]")
    try:
        age = int(input("Age [40]: ") or 40)
        gender = (input("Gender (male/female) [male]: ") or "male").lower()
        smoker = int(input("Smoker (0=no, 1=yes) [0]: ") or 0)
        fever = int(input("Fever Level (0-3) [0]: ") or 0)
        cough = int(input("Cough Level (0-3) [1]: ") or 1)
        shortness_of_breath = int(input("Shortness of breath (0-3) [0]: ") or 0)
        chest_pain = int(input("Chest pain (0-3) [0]: ") or 0)
    except ValueError:
        print("Invalid input. Using defaults.")

    # 4. Feature map (must match 40 symptoms used in training)
    # Filling common ones and defaulting others to 0
    patient_data = {
        "age": age, "gender": gender, "smoker": smoker,
        "heart_rate": 80, "blood_pressure": 120, "cholesterol_level": 180,
        "fever": fever, "cough": cough, "shortness_of_breath": shortness_of_breath,
        "chest_pain": chest_pain, "breathing_difficulty": shortness_of_breath
    }
    
    # Fill remaining columns to reach the 40+ features used in dataset
    # (Simplified for demonstration - in production this mapping is automated)
    placeholder_cols = [
        "fatigue", "headache", "runny_nose", "sore_throat", "body_ache", "nausea", 
        "vomiting", "diarrhea", "dizziness", "chills", "loss_of_smell", "loss_of_taste",
        "wheezing", "rash", "eye_irritation", "ear_pain", "sweating", "joint_pain", 
        "abdominal_pain", "back_pain", "blurred_vision", "dry_cough", "wet_cough", 
        "sinus_pressure", "sneezing", "rapid_heartbeat", "slow_heartbeat", 
        "dehydration", "loss_of_appetite", "sleep_disturbance", "anxiety", 
        "irritability", "muscle_spasm", "skin_redness", "itchiness"
    ]
    for col in placeholder_cols: patient_data[col] = 0

    df = pd.DataFrame([patient_data])

    # 5. Preprocess (DP + Scaling)
    df_dp = apply_dp(df, epsilon=1.0)
    X_num = df_dp.drop(columns=["gender"]) 
    X_num = X_num[list(scaler.feature_names_in_)]
    X_scaled = scaler.transform(X_num)

    # 6. Predict
    prediction = model.predict(X_scaled)[0]
    disease = le.inverse_transform([prediction])[0]

    print("\n" + "-"*30)
    print(f"PREDICTED CONDITION: {disease.upper()}")
    print("-"*30)

if __name__ == "__main__":
    load_and_predict()
