import pandas as pd
from dp.ldp_mechanism import apply_laplace_ldp
from dp.gender_dp import encode_gender, dp_gender_series


def preprocess_model2(csv_path, epsilon):

    df = pd.read_csv(csv_path)

    # Drop irrelevant columns
    drop_cols = [
        "Device Name",
        "Suggestions for health wearable devices.",
        "Date_of_Birth",
        "Fireboult", "Fireboult.1", "Fireboult.2",
        "Fireboult.3", "Fireboult.4",
        "Fireboult.5", "Fireboult.6"
    ]

    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    # Convert Yes/No
    yes_no_map = {"Yes": 1, "No": 0}
    df = df.replace(yes_no_map)

    # Convert Low/Moderate/High
    level_map = {"Low": 0, "Moderate": 1, "High": 2}
    df = df.replace(level_map)

    # ============================
    # 🔥 Binary Target Conversion
    # ============================
    df["disease"] = df["disease"].apply(
        lambda x: 0 if str(x).lower() == "healthy" else 1
    )

    X = df.drop(columns=["disease"])
    y = df["disease"]

    # Identify gender column
    gender_col = None
    for col in X.columns:
        if col.lower() == "gender":
            gender_col = col
            break

    numeric_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()

    if gender_col in numeric_cols:
        numeric_cols.remove(gender_col)

    # Apply Laplace DP
    if numeric_cols:
        X_numeric = X[numeric_cols].astype(float)
        X_numeric_dp = apply_laplace_ldp(X_numeric, epsilon)
    else:
        X_numeric_dp = pd.DataFrame()

    # Apply gender DP
    if gender_col:
        gender_encoded = X[gender_col].apply(encode_gender)
        gender_dp = dp_gender_series(gender_encoded, epsilon)
        X_gender_dp = pd.DataFrame({gender_col: gender_dp})
    else:
        X_gender_dp = pd.DataFrame()

    # Keep other categorical untouched
    other_cols = [
        col for col in X.columns
        if col not in numeric_cols and col != gender_col
    ]

    X_other = X[other_cols].reset_index(drop=True)

    X_final = pd.concat(
        [
            X_numeric_dp.reset_index(drop=True),
            X_gender_dp.reset_index(drop=True),
            X_other
        ],
        axis=1
    )

    return X_final, y
