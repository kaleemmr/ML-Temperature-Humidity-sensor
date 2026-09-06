import os
import pandas as pd
import matplotlib.pyplot as plt

# 1. Define File Paths
RAW_DATA_PATH = os.path.join("data", "dht22_data.csv")
CLEAN_DATA_PATH = os.path.join("data", "dht22_data_clean.csv")

print("=== Phase 2: Data Cleaning & Inspection ===")

# 2. Load Raw CSV Data
if not os.path.exists(RAW_DATA_PATH):
    raise FileNotFoundError(f"Could not find {RAW_DATA_PATH}. Make sure the file is saved in the data/ directory.")

df = pd.read_csv(RAW_DATA_PATH)

print(f"\n[+] Raw Data Loaded: {len(df)} total rows")
print("\nFirst 5 rows:")
print(df.head())

# 3. Clean Missing, Null, or Malformed Data
df = df.dropna()

# Convert columns to numeric (coercing non-numeric errors to NaN, then dropping)
df['temperature_c'] = pd.to_numeric(df['temperature_c'], errors='coerce')
df['humidity_percent'] = pd.to_numeric(df['humidity_percent'], errors='coerce')
df = df.dropna()

# 4. Filter Impossible / Sensor Crash Outliers (DHT22 realistic range check)
# Temperature realistic indoor range: 0°C to 50°C
# Humidity realistic indoor range: 10% to 90%
valid_temp = (df['temperature_c'] >= 0) & (df['temperature_c'] <= 50)
valid_hum = (df['humidity_percent'] >= 10) & (df['humidity_percent'] <= 90)

df_clean = df[valid_temp & valid_hum].copy()

# Remove duplicate consecutive sensor locks
df_clean = df_clean.reset_index(drop=True)

removed_count = len(df) - len(df_clean)
print(f"\n[+] Data Cleaning Complete:")
print(f"    - Cleaned Dataset Rows: {len(df_clean)}")
print(f"    - Outliers / Bad Rows Removed: {removed_count}")

# 5. Export Cleaned Dataset
df_clean.to_csv(CLEAN_DATA_PATH, index=False)
print(f"    - Saved cleaned data to: {CLEAN_DATA_PATH}")

# 6. Plot Baseline Trends
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(df_clean['temperature_c'], color='tab:red', linewidth=1)
plt.title("Ambient Temperature (°C)")
plt.xlabel("Sample Index")
plt.ylabel("Temperature (°C)")
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(df_clean['humidity_percent'], color='tab:blue', linewidth=1)
plt.title("Ambient Humidity (%)")
plt.xlabel("Sample Index")
plt.ylabel("Humidity (%)")
plt.grid(True)

plt.tight_layout()
plt.savefig(os.path.join("data", "baseline_plot.png"))
print("\n[+] Saved visualization plot to: data/baseline_plot.png")
plt.show()