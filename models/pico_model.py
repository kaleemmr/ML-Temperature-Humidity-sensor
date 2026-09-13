

TEMP_MIN = 21.32
TEMP_MAX = 22.48     # models temperature values obtained from raw data before
HUM_MIN = 56.56
HUM_MAX = 65.02      # models humidity values obtained from raw data before

def predict(temp, hum): # obtains the raw inputs for temperature and humidity from the sensor.
    
    if (TEMP_MIN <= temp <= TEMP_MAX) and (HUM_MIN <= hum <= HUM_MAX):
        return 1  # returns 1 if values obtained are within thresholds and are normal.
    else:
        return -1 # returns -1 if values obtained are not within thresholds and are an anomaly.
