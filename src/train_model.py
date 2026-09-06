import os
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

CLEAN_DATA_PATH = os.path.join("data", "dht22_data_clean.csv")
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "isolation_forest.joblib")

print("=== Phase 3: Training Isolation Forest Model ===")

# 1. Load Cleaned Dataset
if not os.path.exists(CLEAN_DATA_PATH):
    raise FileNotFoundError(f"Could not find {CLEAN_DATA_PATH}. Please run src/clean_data.py first.")

df = pd.read_csv(CLEAN_DATA_PATH)
X = df[['temperature_c', 'humidity_percent']]

print(f"[+] Training dataset loaded: {len(df)} samples")

# 2. Instantiate and Train Isolation Forest
# contamination=0.01 sets an expected baseline anomaly threshold of ~1%
model = IsolationForest(
    n_estimators=100,
    contamination=0.01,
    random_state=42
)

model.fit(X)

# 3. Export Model Binary
os.makedirs(MODEL_DIR, exist_ok=True)
joblib.dump(model, MODEL_PATH)

print("\n[+] Model training complete!")
print(f"[+] Exported model binary to: {MODEL_PATH}")