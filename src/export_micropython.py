import os
import joblib
import numpy as np

MODEL_PATH = os.path.join("models", "isolation_forest.joblib")
OUTPUT_PATH = os.path.join("models", "pico_model.py")

model = joblib.load(MODEL_PATH)

print("=== Converting Isolation Forest for MicroPython ===")

# Extract feature medians/bounds directly from estimators for embedded execution
temps = []
hums = []

# Sample space limits learned by trees
for estimator in model.estimators_:
    tree = estimator.tree_
    for feature, threshold in zip(tree.feature, tree.threshold):
        if feature == 0:  # temperature_c
            temps.append(threshold)
        elif feature == 1:  # humidity_percent
            hums.append(threshold)

t_min, t_max = np.percentile(temps, [5, 95])
h_min, h_max = np.percentile(hums, [5, 95])

micropython_code = f"""# Auto-generated Micro-ML Decision Rules for MicroPython
# Derived from Scikit-Learn IsolationForest Model Binary

TEMP_MIN = {t_min:.2f}
TEMP_MAX = {t_max:.2f}
HUM_MIN = {h_min:.2f}
HUM_MAX = {h_max:.2f}

def predict(temp, hum):
    \"\"\"
    Returns 1 for NORMAL, -1 for ANOMALY based on trained tree thresholds.
    \"\"\"
    if (TEMP_MIN <= temp <= TEMP_MAX) and (HUM_MIN <= hum <= HUM_MAX):
        return 1  # Normal
    else:
        return -1 # Anomaly
"""

with open(OUTPUT_PATH, "w") as f:
    f.write(micropython_code)

print(f"[+] Micro-ML module exported successfully: {OUTPUT_PATH}")
print(f"    - Temperature Bounds: {t_min:.1f}°C to {t_max:.1f}°C")
print(f"    - Humidity Bounds: {h_min:.1f}% to {h_max:.1f}%")