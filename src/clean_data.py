import os
import pandas as pd
import matplotlib.pyplot as plt # imports libraries, and python operating system.

# 1. Define file paths
RAW_DATA_PATH = os.path.join("data", "dht22_data.csv")  
CLEAN_DATA_PATH = os.path.join("data", "dht22_data_clean.csv") # i had these files and data paths within vs code and these are defined using concatenation.

print("Data Cleaning.")

# 2. Load raw CSV Data
if not os.path.exists(RAW_DATA_PATH):
    raise FileNotFoundError(f"Could not find {RAW_DATA_PATH}. ") # added to let me know if its properly added or not.

df = pd.read_csv(RAW_DATA_PATH) # reads the raw data, and assigns it to the variable df which is data frame.

print(f"\n[+] Raw Data Loaded: {len(df)} total rows") # prints the number of rows of data and counts it.
print("\nFirst 5 rows:") 
print(df.head()) # prints the first 5 rows of the df which is the head.

df = df.dropna() # any row with anything missing gets removed so no bad data is included.

# Converts columns to numeric (making non-numeric errors to not a number or NaN, then dropping)
df['temperature_c'] = pd.to_numeric(df['temperature_c'], errors='coerce')
df['humidity_percent'] = pd.to_numeric(df['humidity_percent'], errors='coerce')
df = df.dropna() # any row with NaN gets removed so no bad data is included again.

valid_temp = (df['temperature_c'] >= 0) & (df['temperature_c'] <= 50) # makes the temperature range an realistic indoor range: 0°C to 50°C
valid_hum = (df['humidity_percent'] >= 10) & (df['humidity_percent'] <= 90) # makes the humidity range an realistic indoor range: 10% to 90%

df_clean = df[valid_temp & valid_hum].copy() # filters each row in the dataframe, and if both conditions valid_temp and valid_hum are true they pass if not then it isnt flagged as true.

# Remove duplicate consecutive sensor locks
df_clean = df_clean.reset_index(drop=True) # reindexes all the rows to remove missing rows made by removing NaN's and bad rows.

removed_count = len(df) - len(df_clean)  
print(f"Data Cleaning Complete")
print(f"Cleaned Dataset Rows: {len(df_clean)}")
print(f"Outliers / Bad Rows Removed: {removed_count}")

df_clean.to_csv(CLEAN_DATA_PATH, index=False) # writes the new data to a new csv file.
print(f"Saved cleaned data to: {CLEAN_DATA_PATH}")

plt.figure(figsize=(12, 5))  # creates a matplotlib canvas with the width of 12 inches by height in 5 inches.

plt.subplot(1, 2, 1) # grid layout with  1 row and 2 columns and this uses the left side to do plotting from.
plt.plot(df_clean['temperature_c'], color='tab:red', linewidth=1) # plots the red line for temp
plt.title("Ambient Temperature (°C)") # sets the title of the graph
plt.xlabel("Sample Index") # x axis title
plt.ylabel("Temperature (°C)") # y axis title
plt.grid(True) # adds background grid lines which makes it clearer to read.

plt.subplot(1, 2, 2) # switches to right side in the 1 row and 2 column layout
plt.plot(df_clean['humidity_percent'], color='tab:blue', linewidth=1) # plots the blue line for humidity
plt.title("Ambient Humidity (%)") # sets title of the graph
plt.xlabel("Sample Index") # x axis title
plt.ylabel("Humidity (%)") # y axis title
plt.grid(True)  # sets grid background lines
 
plt.tight_layout() # adjusts the spacing between the titles and axis labels so nothing intersects eachother.
plt.savefig(os.path.join("data", "baseline_plot.png")) # renders the graph with data and exports it.
print("Saved visualization plot to: data/baseline_plot.png") # tells me its done it
plt.show() # shows the graph as soon as its done.
