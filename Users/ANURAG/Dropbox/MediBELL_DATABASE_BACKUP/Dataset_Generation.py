import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv("Final_Augmented_dataset_Diseases_and_Symptoms.csv")

# Encode target
le = LabelEncoder()
df['disease'] = le.fit_transform(df['disease'])

# Shuffle dataset
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Get unique diseases
diseases = df['disease'].unique()

# Split diseases into 3 groups (non-IID)
disease_splits = np.array_split(diseases, 3)

clients = {}

for i, d_split in enumerate(disease_splits):
    # Select only subset of diseases for each client
    client_df = df[df['disease'].isin(d_split)]

    # Sample to control size
    client_df = client_df.sample(n=50000, replace=True, random_state=42+i)

    clients[f'client_{i+1}'] = client_df

    # Save dataset
    client_df.to_csv(f'client_{i+1}.csv', index=False)

print("✅ 3 Non-IID Federated Datasets Generated")