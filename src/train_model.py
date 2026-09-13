import os # imports python os
import pandas as pd # imports pandas which will read the cleaned data efficiently
from sklearn.ensemble import IsolationForest # imports a machine learning algorithm in isolationforest
import joblib # this library helps save the trained models.

CLEAN_DATA_PATH = os.path.join("data", "dht22_data_clean.csv") # sets the path for the clean data 
MODEL_DIR = "models" 
MODEL_PATH = os.path.join(MODEL_DIR, "isolation_forest.joblib") # sets the path for where the model will be saved at

print("training model")

# 1. Load Cleaned Dataset
if not os.path.exists(CLEAN_DATA_PATH):
    raise FileNotFoundError(f"Could not find {CLEAN_DATA_PATH}. Please run src/clean_data.py first.") # checks if the clean data is in the right path it needs to be in just in case.

df = pd.read_csv(CLEAN_DATA_PATH) # reads the clean data and puts it into a data frame.
X = df[['temperature_c', 'humidity_percent']] # makes the data frame into a 2d matrix

print(f"Training dataset loaded: {len(df)} samples") # prints total number of clean data row.

# contamination=0.01 sets an expected baseline anomaly threshold of ~1%
model = IsolationForest(
    n_estimators=100, # this makes it so there is 100 different decision trees which are random.
    contamination=0.01, # sets the results with anomalies to 1% 
    random_state=42 # makes model making more accuruate as same random choice sequences are being performed.
)

model.fit(X) # execuutes the isolation forest algorithm onto the 2d matrix 'X',.

os.makedirs(MODEL_DIR, exist_ok=True) # makes the directory model_Dir incase it isnt there, just to be sure there isnt anything that is going to cause errors. error_ok stops error is directory is already there.
joblib.dump(model, MODEL_PATH) # converts the trained model with all the trees and everything into a file.

print("Model training complete!!")
print(f"Exported model to: {MODEL_PATH}")
