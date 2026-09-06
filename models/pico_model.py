# Auto-generated Micro-ML Decision Rules for MicroPython
# Derived from Scikit-Learn IsolationForest Model Binary

TEMP_MIN = 21.32
TEMP_MAX = 22.48
HUM_MIN = 56.56
HUM_MAX = 65.02

def predict(temp, hum):
    """
    Returns 1 for NORMAL, -1 for ANOMALY based on trained tree thresholds.
    """
    if (TEMP_MIN <= temp <= TEMP_MAX) and (HUM_MIN <= hum <= HUM_MAX):
        return 1  # Normal
    else:
        return -1 # Anomaly
