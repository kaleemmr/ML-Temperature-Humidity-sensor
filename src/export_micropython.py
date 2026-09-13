import os
import joblib 
import numpy as np # imports all libraries needed, numpy is here to solve all the complex maths.

MODEL_PATH = os.path.join("models", "isolation_forest.joblib") 
OUTPUT_PATH = os.path.join("models", "pico_model.py") # sets all the maths needed, and makes the new path for the new model to be fully produced and ready for the pico.

model = joblib.load(MODEL_PATH) # loads the isolation forest model into the variable model.

print("converting")

temps = []
hums = [] # empty arrays

# Sample space limits learned by trees
for estimator in model.estimators_: # iterates through each decision tree in the model
    tree = estimator.tree_ # gets access to that specific tree and stores it in the variable tree.
    for feature, threshold in zip(tree.feature, tree.threshold): # features gets the index for each split or leaf node. threshold gets the values. 0 = temp , 1 = humifity, -2 = lead node which is basically nothing        
        if feature == 0:  # temperature_c
            temps.append(threshold)
        elif feature == 1:  # humidity_percent
            hums.append(threshold)

t_min, t_max = np.percentile(temps, [5, 95]) # gets the 5th and 95th percentiles of the split thresholds and these will be dense and full of more normal variance then from 0 and 100% which are really extreme choices.
h_min, h_max = np.percentile(hums, [5, 95])

micropython_code = f"""# 

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
