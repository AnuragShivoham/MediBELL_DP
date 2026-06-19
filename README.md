# MediBELL: Privacy-Preserving IoT Healthcare System

MediBELL is a cutting-edge healthcare AI system designed with a focus on **IoT + Healthcare + Privacy-Preserving AI**. It leverages **Local Differential Privacy (LDP)** and **Federated Learning (FL)** to ensure that sensitive patient data remains protected, secure, and decentralized.

---

## 🚀 Key Features

- **Local Differential Privacy (LDP)**: Protects individual patient records at the edge using the **Laplace Mechanism** (for numeric vitals like age, heart rate, BP) and **Randomized Response** (for binary/categorical attributes like gender, smoker status, and symptom profiles).
- **Advanced Federated Learning (FL)**: Supports decentralized model training across multiple local nodes using the **Federated Averaging (FedAvg)** aggregation algorithm.
- **Deep MLP Architecture**: Leverages Multi-Layer Perceptrons (128-64-32 architecture) to capture complex non-linear symptom combinations and disease correlations.
- **IoT Integration**: Built to simulate and process continuous high-velocity health streams from wearables (Heart Rate, BP, SpO2, etc.).

---

## 🛠 Tech Stack

- **ML/DL Frameworks**: Scikit-Learn (SGDClassifier, MLPClassifier, RandomForestClassifier)
- **Core Logic**: NumPy, Pandas, Joblib, PyYAML
- **Visualization**: Matplotlib

---

## 📂 Project Structure

- `dp/`: Core Local Differential Privacy mechanisms (`ldp_mechanism.py`, `gender_dp.py`).
- `fl/`: Standard federated regression learning logic (Clients, Server, and Utilities).
- `fl_advanced/`: Advanced Deep Learning (MLP) federated structure and production scale simulations.
- `utils/`: Common preprocessing pipelines, config loaders, and predictability layers.
- `tests/`: Automated unit test suite verifying validation modules and privacy bounds.
- `visualizations/`: Generated evaluation plots (e.g., Epsilon tradeoff curves).
- `generate_missing_datasets.py`: Local utility to synthesize clinical/survey data and baseline models.

---

## 📊 Getting Started

### 1. Local Environment Setup
Clone the repository and set up a Python virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Generate Missing Datasets & Baseline Models
Since large CSV datasets and `.pkl` model binaries are excluded by Git (`.gitignore`), generate them locally first:
```bash
.venv/bin/python generate_missing_datasets.py
```
This utility creates:
- Clean clinical datasets (`data/synthetic_dataset_25k_40symptoms.csv`)
- Survey comparison datasets (`data/MODEL_2_MediBELL.csv` and `data/FINAL_DATABASE_MEDIBELL.csv`)
- Un-noised baseline model files under `models/`

### 3. Run Automated Unit Tests
Verify privacy mechanisms and validation structures:
```bash
.venv/bin/python -m unittest discover -s tests -p "test_*.py"
```

---

## 📈 Running Simulations & Experiments

### A. Run the Interactive Menu
To access baseline training, DP model fitting, local evaluation, epsilon budgeting experiments, and interactively predict diseases:
```bash
.venv/bin/python main.py
```

### B. Run the Advanced Production-Scale (25L) FL Simulation
To run a federated Multi-Layer Perceptron (MLP) simulation across three hospital nodes over **2.8 Lakh patient records** under LDP noise:
```bash
.venv/bin/python fl_advanced/run_production_fl.py
```
The aggregated global model weights will be saved to `fl_advanced/production_global_model.pkl`.

### C. Run the Advanced Patient Predictor
Query the trained global model interactively with patient vitals and symptom levels:
```bash
.venv/bin/python fl_advanced/predict_advanced.py
```

### D. Run Epsilon Tradeoff Experiments
Run localized DP evaluation and export tradeoff plots to `visualizations/`:
```bash
# Epsilon tradeoffs (with vs. without DP accuracy)
.venv/bin/python epsilon_experiment.py

# Clinical vs. Survey dataset accuracy degradation comparison
.venv/bin/python dp_comparison_experiment.py
```

---

## 🛡 Privacy & Regulatory Compliance
- **Zero Raw Data Transfer**: Patient records stay on edge nodes; only mathematical weight matrices are shared via FedAvg.
- **Strict Privacy Bounds**: Epsilon ($\epsilon$) controls the math guarantee of individual privacy, protecting against membership inference attacks and ensuring HIPAA/GDPR compliance.
- **Synergy Optimization**: MLP captures non-linear features, minimizing accuracy loss under strict privacy budgets.
